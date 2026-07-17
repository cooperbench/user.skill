> DEVELOPER

create a trail. we want to be able to go the route /leaderboard and it renders the leaderboard there

> AGENT

I’ll use the `trail` skill for this, since you asked to create one. I’ll first read its local instructions, then I’ll trace the app routing shape so the trail matches the repo’s conventions.

> TOOL

tool_use exec_command
id: call_tfjgINO7gGZiSNTkBMMGBR04
```json
{
  "cmd": "sed -n '1,240p' /home/<USER>/Documents/work/planetfall-seed-signalkit/.codex/skills/trail/SKILL.md",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_lEs7MQglSVU8ewhIad0xKfap
```json
{
  "cmd": "pwd && rg --files -g '!*node_modules*' -g '!*.png' -g '!*.jpg' -g '!*.jpeg' -g '!*.gif' | sed -n '1,220p'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_tfjgINO7gGZiSNTkBMMGBR04
```
Chunk ID: 7efb65
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1792
Output:
---
name: trail
description: Use when a discovery cycle has converged on a spec/design doc and work is about to move into implementation, or when the user types /trail or asks to create, view, or update an Entire "trail". Also use when asked to capture the intent of a piece of work, or to attach a branch's sessions/checkpoints to a trail. Manages trails via `entire trail`.
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Trail

Capture the *Entire context* of a piece of work as a **trail** - the intent ("why/what"), with the branch's checkpoints/sessions as the evidence ("how/when"). Create one at spec-time via `entire trail`.

## The one rule that governs everything

A trail is keyed to a **single branch**. Checkpoints carry no trail link - the backend associates them **dynamically, by branch name**, at read time. Verified rule:

> A checkpoint appears under the trail **iff its commit is on the trail's branch and *ahead of the base*** - commits also on the base are excluded. "On the base" means recorded server-side, i.e. **pushed to `origin/<base>`**.

What […]

> TOOL

tool_result
id: call_lEs7MQglSVU8ewhIad0xKfap
```
Chunk ID: 71fecd
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 158
Output:
/home/<USER>/Documents/work/planetfall-seed-signalkit
src/memoryProps.js
src/debris.js
src/islandView.js
src/noise.js
src/overhead.js
src/planetView.js
src/planet.js
src/atmosphere.js
src/ring.js
src/style.css
src/fallingProps.js
src/main.js
src/three-utils.js
src/levelOneRecords.js
src/leaderboardPanel.js
src/leaderboard.js
src/titleScreen.js
src/terrain.js
src/launchView.js
src/archiveView.js
src/firstPerson.js
src/droneBayView.js
src/sfx.js
PLAN.md
api/leaderboard.test.js
api/leaderboard.js
CONTRIBUTING.md
package.json
package-lock.json
public/audio/asteroid-circuit.mp3
README.md
vite.config.js
LICENSE
index.html

```

> AGENT

The repo is a small Vite app, and it already has leaderboard modules, so the intent is nice and concrete. I’m checking the existing plan and branch state now so the trail attaches to the right branch instead of floating loose.

> TOOL

tool_use exec_command
id: call_8w048OausZcp4S49TLlZ2Itd
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_4NohZGc0zBeCBL9TN9B6l79Y
```json
{
  "cmd": "git branch --show-current",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_nio9bqSecHCMWcyTCwrOxqsR
```json
{
  "cmd": "sed -n '1,260p' PLAN.md",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_Nbdkp17rQimxRIMpZJzHohaM
```json
{
  "cmd": "git remote -v",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_KFcMkyWelvyx4hWc3nAM8AP0
```json
{
  "cmd": "entire trail show",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_8w048OausZcp4S49TLlZ2Itd
```
Chunk ID: 25a301
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 9
Output:
## main...origin/main
?? .codex/

```

> TOOL

tool_result
id: call_4NohZGc0zBeCBL9TN9B6l79Y
```
Chunk ID: 70f164
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2
Output:
main

```

> TOOL

tool_result
id: call_nio9bqSecHCMWcyTCwrOxqsR
```
Chunk ID: 8334ae
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2610
Output:
# Planetfall - Plan & Status

_Last updated: 2026-06-18_

## Current Status

Planetfall is now a playable three-level browser game, plus a shelved archive
level and a Vercel/Neon leaderboard path.

The current game is no longer the early "walk around one island collecting
artifacts" prototype. The shipped arc is:

1. **Level 1 - First Memories:** fixed-camera salvage cannon, falling records,
   terminal banking, checkpoint list review.
2. **Level 2 - The Drone Bay:** command-pass/order-ticket rush with dispatch
   pips, drones, conveyor blocks, `entire checkpoint explain`, drag-to-match,
   and `entire dispatch`.
3. **Level 3 - Launch Clearance:** cockpit finale with command/skill tool
   choices, record-backed answers, launch code, ignition, and liftoff.

The title screen, rebellion intro, TV effect, music/SFX options, score saving
UI, and top-10 leaderboard screen are also built.

## Pitch

You are a downed pilot. Your ship survived the crash, but its records are
scattered across the planet. Recovering those records in-fiction is the same
act as recovering useful context from a real project history with Entire.

Teaching arc:

- **Level 1:** bank your own work. A commit freezes it; a checkpoint […]

> TOOL

tool_result
id: call_Nbdkp17rQimxRIMpZJzHohaM
```
Chunk ID: 6160bf
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 40
Output:
origin	https://github.com/blackgirlbytes/planetfall-seed-signalkit.git (fetch)
origin	https://github.com/blackgirlbytes/planetfall-seed-signalkit.git (push)

```

> TOOL

tool_result
id: call_KFcMkyWelvyx4hWc3nAM8AP0
```
Chunk ID: 49e1bb
Wall time: 0.6238 seconds
Process exited with code 1
Original token count: 28
Output:
no trail found for current branch "main"
hint: run 'entire trail create' or 'entire trail list --status any'

```

> AGENT

There’s no existing trail on `main`, and `PLAN.md` already names the current leaderboard architecture. Since this is active implementation intent, I’m going to create an open trail on a feature branch `codex/leaderboard-route` with `PLAN.md` as the linked spec/status source.

> TOOL

tool_use exec_command
id: call_SDVKJxMl0VVU0mA6Bn1pQYIv
```json
{
  "cmd": "git symbolic-ref --short refs/remotes/origin/HEAD || true",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_E3SB5Pm1ffKlF85edCHq5Lr8
```json
{
  "cmd": "git log --oneline origin/main..HEAD",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_hHE3aenalAhRe2oyksN7JhiD
```json
{
  "cmd": "git branch --list 'codex/leaderboard-route'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_SDVKJxMl0VVU0mA6Bn1pQYIv
```
Chunk ID: 93b566
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 3
Output:
origin/main

```

> TOOL

tool_result
id: call_E3SB5Pm1ffKlF85edCHq5Lr8
```
Chunk ID: 69945a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_hHE3aenalAhRe2oyksN7JhiD
```
Chunk ID: eccecb
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 0
Output:

```

> AGENT

I found no local commits ahead of `origin/main`, so there’s nothing stranded on the base branch. Creating the trail now will also switch us onto the feature branch, which is the right place for the implementation checkpoints to gather.

> TOOL

tool_use exec_command
id: call_mUEuwsHkRvYqpphMszgbowuI
```json
{
  "cmd": "body=$(cat <<'EOF'\nAdd a direct browser route so visiting /leaderboard renders the existing leaderboard experience without needing to enter through the title menu. Preserve the current score API, title-screen leaderboard wiring, and game progression behavior.\n\nSpec: PLAN.md\nEOF\n)\nentire trail create --status open --branch codex/leaderboard-route --checkout --title \"Render leaderboard at /leaderboard\" --body \"$body\"",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 30000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_mUEuwsHkRvYqpphMszgbowuI
```
Chunk ID: 8cc586
Wall time: 3.5645 seconds
Process exited with code 0
Original token count: 65
Output:
Created branch codex/leaderboard-route
Pushed branch codex/leaderboard-route to origin
Created trail "Render leaderboard at /leaderboard" for branch codex/leaderboard-route (ID: 019ee0a3-af9a-74e7-af75-00d0f1e20b66)
Switched to branch codex/leaderboard-route

```

> AGENT

Trail creation succeeded and pushed the branch. I’m doing one quick verification pass so I can hand you the exact trail and branch state cleanly.

> TOOL

tool_use exec_command
id: call_tMmpqBaDao5sk0jzrN0IJBPD
```json
{
  "cmd": "entire trail show",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_25RPfQDIZhCP9QQ1K9lu27gx
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_tMmpqBaDao5sk0jzrN0IJBPD
```
Chunk ID: 165389
Wall time: 0.2739 seconds
Process exited with code 0
Original token count: 70
Output:
Trail: Render leaderboard at /leaderboard
  Number:  2
  ID:      019ee0a3-af9a-74e7-af75-00d0f1e20b66
  Branch:  codex/leaderboard-route
  Base:    main
  Status:  open
  Author:  blackgirlbytes
  Phase:   planning
  Created: 2026-06-19T16:08:03Z
  Updated: 2026-06-19T16:08:03Z

```

> TOOL

tool_result
id: call_25RPfQDIZhCP9QQ1K9lu27gx
```
Chunk ID: 5d0f93
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 18
Output:
## codex/leaderboard-route...origin/codex/leaderboard-route
?? .codex/

```

> AGENT

Created the trail for the `/leaderboard` route work.

Trail: `#2` “Render leaderboard at /leaderboard”  
Branch: `codex/leaderboard-route`  
Status: `open`  
Spec linked in body: `PLAN.md`

The branch was created, checked out, and pushed to origin. Existing untracked `.codex/` files were left untouched.

::git-create-branch{cwd="/home/<USER>/Documents/work/planetfall-seed-signalkit" branch="codex/leaderboard-route"}
::git-push{cwd="/home/<USER>/Documents/work/planetfall-seed-signalkit" branch="codex/leaderboard-route"}

> DEVELOPER

link me to the trail please

> AGENT

I’ll pull the trail metadata from `entire` rather than guessing the web URL shape.

> TOOL

tool_use exec_command
id: call_fLQ7M9ML3TE9y7Ti4j8uHHFh
```json
{
  "cmd": "entire trail show --help",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_dFu4kOtmFMngfMli5IgJjzDO
```json
{
  "cmd": "entire trail list --status any --json -n 20",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_fLQ7M9ML3TE9y7Ti4j8uHHFh
```
Chunk ID: 9d1946
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 60
Output:
Show a trail.

If <trail> is omitted, shows the trail for the current branch. Otherwise,
<trail> may be a trail number, id, or branch in the current repo.

Usage:
  entire trail show [<trail>] [flags]

Flags:
  -h, --help   help for show

```

> TOOL

tool_result
id: call_dFu4kOtmFMngfMli5IgJjzDO
```
Chunk ID: 6e6933
Wall time: 0.6337 seconds
Process exited with code 0
Original token count: 266
Output:
[
  {
    "number": 2,
    "trail_id": "019ee0a3-af9a-74e7-af75-00d0f1e20b66",
    "branch": "codex/leaderboard-route",
    "base": "main",
    "title": "Render leaderboard at /leaderboard",
    "body": "",
    "status": "open",
    "phase": "planning",
    "author": {
      "id": "019d3218-f519-7024-90c8-802e56a5128f",
      "login": "blackgirlbytes"
    },
    "assignees": [],
    "labels": [],
    "created_at": "2026-06-19T16:08:03.094Z",
    "updated_at": "2026-06-19T16:08:03.094Z",
    "merged_at": null,
    "priority": "none"
  },
  {
    "number": 1,
    "trail_id": "019edf9a-4d86-7ce8-a7fe-dcea690dc5e9",
    "branch": "create-a-level-4",
    "base": "main",
    "title": "Create a level 4",
    "body": "",
    "status": "closed",
    "author": {
      "id": "019d3218-f519-7024-90c8-802e56a5128f",
      "login": "blackgirlbytes"
    },
    "assignees": [
      "blackgirlbytes"
    ],
    "labels": [],
    "created_at": "2026-06-19T11:18:11.07Z",
    "updated_at": "2026-06-19T15:52:44.757Z",
    "merged_at": null,
    "priority": "none"
  }
]

```

> AGENT

The JSON gives the trail ID and number but not the URL, so I’m checking the CLI’s web/open commands now.

> TOOL

tool_use exec_command
id: call_6SmDRxsEJAdxNog8t4KuOvBp
```json
{
  "cmd": "entire --help",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_BhQ0d90CxmLgYt92aAUY24PA
```json
{
  "cmd": "entire trail --help",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_bL6WlXXazCZt2RSD2Z4rpMXn
```json
{
  "cmd": "entire config --help",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_6SmDRxsEJAdxNog8t4KuOvBp
```
Chunk ID: fc56ec
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 463
Output:
The command-line interface for Entire

Getting Started:
  To get started with Entire CLI, run 'entire enable' to enable
  session tracking in your repository, then 'entire agent add <name>'
  to install hooks for a specific agent. For more information, visit:
  https://docs.entire.io/overview


Environment Variables:
  ACCESSIBLE    Set to any value (e.g., ACCESSIBLE=1) to enable accessibility
                mode. This uses simpler text prompts instead of interactive
                TUI elements, which works better with screen readers.

Usage:
  entire [flags]
  entire [command]

Available Commands:
  activity               Show your activity overview
  agent                  Manage agent integrations (add, remove, list)
  auth                   Manage authentication
  checkpoint             Inspect and search checkpoints
  clean                  Clean up Entire session data
  configure              Update Entire settings in the current repository
  disable                Disable Entire in current repository
  dispatch               Generate a dispatch summarizing recent agent work
  doctor                 Diagnose and fix session issues
  enable                 Enable Entire in current repository
  help                   Help about any command
  labs                   Explore experimental Entire workflows
  login                  Log in to Entire
  logout                 Log out of Entire
  plugin                 Manage Entire plugins (install, list, remove)
  recap                  Summarize recent checkpoint activity
  session                Manage agent sessions tracked by Entire
  status                 Show Entire status […]

> TOOL

tool_result
id: call_BhQ0d90CxmLgYt92aAUY24PA
```
Chunk ID: d12f24
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 156
Output:
Trails are branch-centric work tracking abstractions. They describe the
"why" and "what" of your work, while checkpoints capture the "how" and "when".

Usage:
  entire trail [flags]
  entire trail [command]

Available Commands:
  create      Create a trail for the current or a new branch
  delete      Delete a trail
  finding     Manage a trail's agent findings
  list        List recent trails
  show        Show a trail
  update      Update trail metadata
  watch       Tail a trail's finding events live

Flags:
  -h, --help   help for trail

Use "entire trail [command] --help" for more information about a command.

```

> TOOL

tool_result
id: call_bL6WlXXazCZt2RSD2Z4rpMXn
```
Chunk ID: df417b
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 329
Output:
Usage:
  entire
  entire [command]

Available Commands:
  activity               Show your activity overview
  agent                  Manage agent integrations (add, remove, list)
  auth                   Manage authentication
  checkpoint             Inspect and search checkpoints
  clean                  Clean up Entire session data
  configure              Update Entire settings in the current repository
  disable                Disable Entire in current repository
  dispatch               Generate a dispatch summarizing recent agent work
  doctor                 Diagnose and fix session issues
  enable                 Enable Entire in current repository
  help                   Help about any command
  labs                   Explore experimental Entire workflows
  login                  Log in to Entire
  logout                 Log out of Entire
  plugin                 Manage Entire plugins (install, list, remove)
  recap                  Summarize recent checkpoint activity
  session                Manage agent sessions tracked by Entire
  status                 Show Entire status
  version                Show build information

Use "entire [command] --help" for more information about a command.

Error: Invalid usage: unknown command "config" for "entire"

Did you mean this?
	configure


```

> AGENT

No dedicated `trail open` command is exposed here. I’m going to look at the local Entire config/cache for the app URL pattern and then I’ll give you the direct link.

> TOOL

tool_use exec_command
id: call_ybkgY0IZu1n3ohq5yUT3cUF3
```json
{
  "cmd": "rg -n \"entire|trail|app|web|url|api\" .entire .git .codex 2>/dev/null | sed -n '1,240p'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_ul2ktXdT0qI2x6Yi17avhubU
```json
{
  "cmd": "find \"$HOME\" -maxdepth 3 \\( -name '*entire*' -o -name '.entire' \\) -print 2>/dev/null | sed -n '1,240p'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_M9LtJv26ycKfTH88oeWHIzhV
```json
{
  "cmd": "entire status",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_ybkgY0IZu1n3ohq5yUT3cUF3
```
Chunk ID: d0593f
Wall time: 0.1183 seconds
Process exited with code 0
Original token count: 9854
Output:
.codex/agents/entire-search.toml:1:name = "entire-search"
.codex/agents/entire-search.toml:2:description = "Search Entire checkpoint history and transcripts with `entire search --json`. Use proactively when the user asks about previous work, commits, sessions, prompts, or historical context in this repository."
.codex/agents/entire-search.toml:8:Your only history-search mechanism is the `entire search --json` command. Never run `entire search` without `--json`; it opens an interactive TUI. Do not fall back to `rg`, `grep`, `find`, `git log`, or ad hoc codebase browsing when the task is asking for historical search across Entire checkpoints and transcripts.
.codex/agents/entire-search.toml:10:If `entire search --json` cannot run because authentication is missing, the repository is not set up correctly, or the command fails, stop and return a short prerequisite message. Do not make repo changes.
.codex/agents/entire-search.toml:15:1. Turn the task into one or more focused `entire search --json` queries.
.codex/agents/entire-search.toml:16:2. Always use machine-readable output via `entire search --json`.
.codex/agents/entire-search.toml:18:4. If results are broad, rerun `entire search --json` with a narrower query instead of switching tools.
.codex/hooks.json:9:            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks claude-code pre-task'"
.codex/hooks.json:20:            "command": "sh -c 'if […]

> TOOL

tool_result
id: call_ul2ktXdT0qI2x6Yi17avhubU
```
Chunk ID: 12c6bd
Wall time: 0.4207 seconds
Process exited with code 0
Original token count: 712
Output:
/home/<USER>/.config/entire
/home/<USER>/.cursor/projects/Users-goose-guest-Documents-work-entire-io-frontend
/home/<USER>/.cursor/projects/Users-goose-guest-Documents-work-entire-io
/home/<USER>/go/bin/git-remote-entire
/home/<USER>/go/bin/entire
/home/<USER>/.local/bin/entire-dev
/home/<USER>/.local/bin/git-remote-entire
/home/<USER>/.local/bin/entire-agent-goose
/home/<USER>/.local/bin/entire-0.7.6.bak
/home/<USER>/.local/bin/entire
/home/<USER>/.claude/projects/-Users-goose-guest-Documents-agent-experiments-entire-subagent-experiments-claude-with-entire
/home/<USER>/.claude/projects/-Users-goose-guest-Documents-work-entire-io
/home/<USER>/.claude/projects/-Users-goose-guest-Documents-agent-experiments-entire-subagent-experiments-claude-without-entire
/home/<USER>/.claude/projects/-Users-goose-guest-Documents-agent-experiments-entire-subagent-experiments-claude-without-entire-2
/home/<USER>/.claude/projects/-Users-goose-guest-Documents-agent-experiments-entire-subagent-experiments-claude-with-entire-2
/home/<USER>/.codex/skills/using-entire
/home/<USER>/Documents/work/entire-docs
/home/<USER>/Documents/work/entire.io
/home/<USER>/Documents/work/entiredb
/home/<USER>/Documents/agent-experiments/entire-game
/home/<USER>/Documents/agent-experiments/entire-subagent-experiments
/home/<USER>/Documents/agent-experiments/test-goose-entire
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash.png
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash.pdf
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (2).png
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (3).png
/home/<USER>/Downloads/entire-brand-kit
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (4).png
/home/<USER>/Downloads/entireblame.mp4
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (5).png
/home/<USER>/Downloads/entirewhy.mp4
/home/<USER>/Downloads/entirerecap.mp4
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (6).png
/home/<USER>/Downloads/entire-brand-kit.zip
/home/<USER>/Downloads/curl -fsSL entire.ioinstall.sh  bash.pptx
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (7).png
/home/<USER>/Downloads/transcript-entireio-cli-4d570a00-2bd.md
/home/<USER>/Downloads/entire-bundle-20260518-233637 3.zip
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (1).png
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash (1).pdf
/home/<USER>/Downloads/Copy of curl -fsSL entire.ioinstall.sh  bash.pptx
/home/<USER>/.cache/entire

```

> TOOL

tool_result
id: call_M9LtJv26ycKfTH88oeWHIzhV
```
Chunk ID: 93cbdf
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2320
Output:
● Enabled · manual-commit · branch codex/leaderboard-route
  Agents · Claude Code, Codex

── Active Sessions ─────────────────────────────────────────

Codex (gpt-5.5) · 019ee09f-d2c6-72b1-94dd-f0863fe8464a
> "link me to the trail please"
started 2m ago · active now

Codex (gpt-5.5) · 019ee092-5d6c-7481-b301-b1d6cd77de0e
> "check out main and pull the latest"
started 20m ago
! tracking diverged from current HEAD after git history movement

Codex (gpt-5.5) · 019edfb7-5b5b-7d23-9883-c5446a3823b8
> "tell me about how this project evolved"
started 4h ago · stale (run 'entire doctor')
! tracking diverged from current HEAD after git history movement

Codex (gpt-5.5) · 019edfb1-47e4-7933-acbc-2c230b84fe33
> "okay can you create a PR for it"
started 4h ago · active 1h ago · tokens 8138.7k · stale (run 'entire doctor')
! tracking diverged from current HEAD after git history movement

Codex (gpt-5.5) · 019edfaf-d18c-73d0-b7dc-f2d91b48d0e1
> "# Files mentioned by the user: ## --- name: trail descrip..."
started 4h ago · tokens 274.7k · stale (run 'entire doctor')
! tracking diverged from current HEAD after git history movement

Codex (gpt-5.5) · 019edf9f-acdb-7840-b8f9-88f544de7883
> "work on this trail please..https://entire.io/gh/blackgirl..."
started 4h ago · stale (run […]

> AGENT

Here you go: [Trail #2: Render leaderboard at /leaderboard](https://entire.io/gh/blackgirlbytes/planetfall-seed-signalkit/trails/2)

> DEVELOPER

can you work on that trail like execute it

> AGENT

I’ll execute the trail now: first I’m re-reading the trail instructions for this turn, then I’ll inspect the current leaderboard/title routing and patch the smallest path that gives `/leaderboard` a real screen.

> TOOL

tool_use exec_command
id: call_jfbzIOZAgZ1pIeftYakZc3LE
```json
{
  "cmd": "sed -n '1,240p' /home/<USER>/Documents/work/planetfall-seed-signalkit/.codex/skills/trail/SKILL.md",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_kgPU7HgFIQqnWQOPka2RvuhF
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_zsLLxIgg9CjdGkqDe0R5enNt
```json
{
  "cmd": "entire trail show",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result
id: call_jfbzIOZAgZ1pIeftYakZc3LE
```
Chunk ID: 3f8cb1
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1792
Output:
---
name: trail
description: Use when a discovery cycle has converged on a spec/design doc and work is about to move into implementation, or when the user types /trail or asks to create, view, or update an Entire "trail". Also use when asked to capture the intent of a piece of work, or to attach a branch's sessions/checkpoints to a trail. Manages trails via `entire trail`.
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Trail

Capture the *Entire context* of a piece of work as a **trail** - the intent ("why/what"), with the branch's checkpoints/sessions as the evidence ("how/when"). Create one at spec-time via `entire trail`.

## The one rule that governs everything

A trail is keyed to a **single branch**. Checkpoints carry no trail link - the backend associates them **dynamically, by branch name**, at read time. Verified rule:

> A checkpoint appears under the trail **iff its commit is on the trail's branch and *ahead of the base*** - commits also on the base are excluded. "On the base" means recorded server-side, i.e. **pushed to `origin/<base>`**.

What […]

> TOOL

tool_result
id: call_kgPU7HgFIQqnWQOPka2RvuhF
```
Chunk ID: 5a1de4
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 18
Output:
## codex/leaderboard-route...origin/codex/leaderboard-route
?? .codex/

```

> TOOL

tool_result
id: call_zsLLxIgg9CjdGkqDe0R5enNt
```
Chunk ID: 3f688e
Wall time: 1.1661 seconds
Process exited with code 0
Original token count: 70
Output:
Trail: Render leaderboard at /leaderboard
  Number:  2
  ID:      019ee0a3-af9a-74e7-af75-00d0f1e20b66
  Branch:  codex/leaderboard-route
  Base:    main
  Status:  open
  Author:  blackgirlbytes
  Phase:   planning
  Created: 2026-06-19T16:08:03Z
  Updated: 2026-06-19T16:08:03Z

```

> AGENT

We’re on the trail branch and the trail is open. I’m reading the route/menu/leaderboard pieces now so the `/leaderboard` entry uses the existing board instead of inventing a parallel one.

> TOOL

tool_use exec_command
id: call_ETDDnwi9PXTgV4DWK3hZ3Xfw
```json
{
  "cmd": "sed -n '1,260p' src/main.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_tZsW1NCYIJqW5U7RC4dAYzBR
```json
{
  "cmd": "sed -n '1,260p' src/titleScreen.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_I4EndEojs4BSA72E7jczSAHo
```json
{
  "cmd": "sed -n '1,260p' src/leaderboardPanel.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_3mv18eCRu20veL8PjN0zVlgP
```json
{
  "cmd": "sed -n '1,240p' src/leaderboard.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 26000
}
```

> TOOL

tool_result
id: call_ETDDnwi9PXTgV4DWK3hZ3Xfw
```
Chunk ID: efab78
Wall time: 0.0002 seconds
Process exited with code 0
Original token count: 2467
Output:
import * as THREE from "three";
import { createPlanetView } from "./planetView.js";
import { createIslandView } from "./islandView.js";
import { createDroneBayView } from "./droneBayView.js";
import { createArchiveView } from "./archiveView.js";
import { createLaunchView } from "./launchView.js";
import { createTitleScreen } from "./titleScreen.js";
import { loadLeaderboard } from "./leaderboard.js";
import { createLeaderboardPanel } from "./leaderboardPanel.js";
import { sfx } from "./sfx.js";

const canvas = document.getElementById("scene");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.92;
renderer.outputColorSpace = THREE.SRGBColorSpace;

// ---------- background music ----------
const bgm = document.getElementById("bgm");
const audioPanel = document.getElementById("audio-panel");
const audioToggle = document.getElementById("audio-toggle");
const audioMute = document.getElementById("audio-mute");
const audioVolume = document.getElementById("audio-volume");
let userPausedMusic = false;

if (bgm && audioPanel && audioToggle && audioMute && audioVolume) {
  bgm.volume = Number(audioVolume.value);
  bgm.autoplay = true;
  bgm.loop = true;

  const updateAudioUi = () => {
    const playing = !bgm.paused;
    const awaitingStart = !playing && !userPausedMusic;
    audioPanel.classList.toggle("is-awaiting-start", awaitingStart);
    audioToggle.classList.toggle("is-playing", playing);
    audioToggle.setAttribute("aria-label", playing ? "Pause music" : "Start music");
    audioToggle.title = playing ? "Pause music" : "Start music";
    audioMute.classList.toggle("is-muted", bgm.muted || bgm.volume === 0);
    audioMute.setAttribute("aria-label", […]

> TOOL

tool_result
id: call_tZsW1NCYIJqW5U7RC4dAYzBR
```
Chunk ID: 0a001c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2227
Output:
// Title screen — the arcade boot menu shown over the orbit view on first
// load. START GAME dismisses it; OPTIONS holds CONTROLS and SOUND. Sound
// drives the existing #audio-panel controls (the canonical music state) so
// this menu and the in-game panel can never disagree.
// The opening story — a transmission from the rebellion, addressed to the
// downed pilot (the player). It hands the player a mission without naming any
// gameplay so the levels can change underneath it. In three beats, it explains
// the crash, gives the mission, and ends by promoting "Pilot" to "rebel".
const STORY_BEATS = [
  "Pilot, if you can read this, your ship survived the crash, but it needs repairs.",
  "Your ship's records are scattered across the planet. Your mission: recover the records and repair the ship.",
  "Click the landing marker to begin. See you soon, rebel.",
];

import { sfx } from "./sfx.js";

export function createTitleScreen({ onLeaderboard, onStoryStart, onStart } = {}) {
  const root = document.getElementById("title-screen");
  const screens = {
    main: document.getElementById("ts-main"),
    options: document.getElementById("ts-options"),
    controls: document.getElementById("ts-controls"), […]

> TOOL

tool_result
id: call_I4EndEojs4BSA72E7jczSAHo
```
Chunk ID: de54eb
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1657
Output:
import { saveLeaderboardEntry } from "./leaderboard.js";

let panelCount = 0;

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[ch]);
}

export function createLeaderboardPanel({ mount, onClose } = {}) {
  const id = `leaderboard-${++panelCount}`;
  const panel = document.createElement("div");
  panel.className = "leaderboard hidden";
  panel.innerHTML = `
    <div class="lb-head">
      <div>
        <div class="lb-kicker" data-lb-kicker>Your result</div>
        <div class="lb-title" data-lb-title>Game over</div>
      </div>
      <div class="lb-score" data-lb-score>Score 0</div>
    </div>
    <div class="lb-entry" data-lb-entry>
      <p class="lb-copy">Enter a username to save your score.</p>
      <form class="lb-form" data-lb-form>
        <label for="${id}-name">Username</label>
        <div class="lb-submit-row">
          <input id="${id}-name" name="username" type="text" maxlength="18" autocomplete="nickname" spellcheck="false" placeholder="username" />
          <button type="submit">Save score</button>
        </div>
      </form>
    </div>
    <div class="lb-board hidden" data-lb-board>
      <div class="lb-board-label">Top 10 overall</div>
      <div class="lb-table-head" aria-hidden="true">
        <span>#</span><span>Name</span><span>Score</span>
        <span>#</span><span>Name</span><span>Score</span>
      </div>
      <ol class="lb-list" data-lb-list></ol>
      <button class="lb-back" type="button" data-lb-back>Back</button>
    </div>
    <div class="lb-status" data-lb-status></div>
  `;
  mount?.appendChild(panel);

  const kickerEl = panel.querySelector("[data-lb-kicker]");
  const titleEl = panel.querySelector("[data-lb-title]");
  const scoreEl = panel.querySelector("[data-lb-score]");
  const entryEl = panel.querySelector("[data-lb-entry]");
  const boardEl = panel.querySelector("[data-lb-board]");
  const boardLabelEl = panel.querySelector(".lb-board-label");
  const formEl = panel.querySelector("[data-lb-form]");
  const inputEl = panel.querySelector("input");
  const submitEl = panel.querySelector("button[type='submit']");
  const backEl = panel.querySelector("[data-lb-back]");
  const statusEl = panel.querySelector("[data-lb-status]");
  const listEl = panel.querySelector("[data-lb-list]"); […]

> TOOL

tool_result
id: call_3mv18eCRu20veL8PjN0zVlgP
```
Chunk ID: 4a41b4
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1307
Output:
const API_PATH = "/api/leaderboard";
const DISPLAY_LIMIT = 10;
const MAX_LEVEL = 3;

const LEVEL_BASE = {
  1: 0,
  2: 50,
  3: 100,
};
const PROGRESS_POINTS = 10;
const EXTRA_PROGRESS_POINTS = 3;
const GAME_CLEAR_BONUS = 50;
const SPEED_POINTS = 1;
const MISTAKE_PENALTY = 5;
const DURATION_PENALTY_SECONDS = 10;

function canUseRemoteApi() {
  return !import.meta.env?.DEV || import.meta.env?.VITE_USE_REMOTE_LEADERBOARD === "1";
}

function clampInt(value, fallback = 0) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(0, Math.round(n));
}

function clampLevel(value) {
  const level = clampInt(value, MAX_LEVEL);
  return Math.min(MAX_LEVEL, Math.max(1, level));
}

export function computeLeaderboardScore(entry) {
  const level = clampLevel(entry.level ?? entry.levelReached);
  const completed = clampInt(entry.progressCompleted ?? entry.questionsCompleted);
  const total = Math.max(1, clampInt(entry.progressTotal, level === MAX_LEVEL ? 3 : 1));
  const requiredProgress = Math.min(completed, total);
  const extraProgress = Math.max(0, completed - total);
  const completedGame = Boolean(entry.completedGame) || (entry.outcome === "win" && level === MAX_LEVEL);
  const speedBonus = completedGame ? clampInt(entry.timeRemaining) * SPEED_POINTS : 0;
  const clearBonus = completedGame ? GAME_CLEAR_BONUS : 0;
  const mistakePenalty = clampInt(entry.mistakes) * MISTAKE_PENALTY;
  const durationPenalty = completedGame || completed <= 0
    ? 0
    : Math.floor(clampInt(entry.durationSeconds) / DURATION_PENALTY_SECONDS);

  return […]

> AGENT

I’ve got the shape: the existing board is created in `main.js` for the title menu, and it can already load/show rows independently. I’m going to add a path-aware standalone leaderboard mode that enters on `/leaderboard`, keeps the orbit backdrop, and returns home from the Back button.

> TOOL

tool_use exec_command
id: call_j4fNGfpbiYO6mx0E5Xj1jow4
```json
{
  "cmd": "sed -n '260,620p' src/main.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_use exec_command
id: call_HAh5qxb1rC4EgenzInXkA5j5
```json
{
  "cmd": "sed -n '260,560p' src/titleScreen.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_durdnoZRsLEBQCC6m8HGfUY4
```json
{
  "cmd": "sed -n '1,260p' index.html",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_sxQcFfD7h3G01gcWbjeC8AKM
```json
{
  "cmd": "rg -n \"leaderboard|title-up|hidden|lb-\" src/style.css src/*.js index.html",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result
id: call_j4fNGfpbiYO6mx0E5Xj1jow4
```
Chunk ID: 795d36
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 584
Output:
// When the story starts, bring the landing marker into the transmission shot
// and hold it there. The final beat can then tell the player to click what is
// already on screen.
const titleScreen = createTitleScreen({
  onLeaderboard: showTitleLeaderboard,
  onStoryStart: () => {
    planetView.reframe();
    planetView.setLandingMarkerHold(true);
  },
  onStart: () => planetView.setLandingMarkerHold(false),
});
if (!requestedView && !params.get("level") && !endShortcut) titleScreen.show();

// ---------- fade transition ----------
const fade = document.getElementById("fade");
const hint = document.getElementById("hint");
const pin = document.getElementById("island-pin");
let transitioning = false;

function refreshOrbitHud() {
  hint.classList.toggle("hidden", current !== planetView);
  hint.textContent = level2Done
    ? "The launch window is open — the ship is asking for you. Click the pin to board"
    : level1Done
    ? "A new signal — the ship's drone bay just woke up. Click the pin to land"
    : "Drag to orbit · Scroll to zoom · Click the pin to land";
  pin?.classList.toggle("is-corrupted", level1Done && !level2Done);
}
refreshOrbitHud();

function switchTo(view) {
  if (transitioning || view === current) return;
  transitioning = true;
  fade.classList.add("show");
  setTimeout(() => {
    current.exit();
    current = view;
    current.enter();
    refreshOrbitHud();
    fade.classList.remove("show");
    transitioning = false;
  }, 650); // match #fade […]

> TOOL

tool_result
id: call_HAh5qxb1rC4EgenzInXkA5j5
```
Chunk ID: 34d430
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 36
Output:
    root.classList.add("is-leaving");
    setTimeout(() => root.classList.add("hidden"), 650); // match the CSS fade
  }

  return { show };
}

```

> TOOL

tool_result
id: call_durdnoZRsLEBQCC6m8HGfUY4
```
Chunk ID: d1e051
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 3283
Output:
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Planetfall</title>
    <link rel="stylesheet" href="/src/style.css" />
  </head>
  <body>
    <canvas id="scene"></canvas>

    <div id="ui">
      <header id="hud">
        <div class="hud-title">PLANETFALL</div>
      </header>

      <div id="hint">Drag to orbit · Scroll to zoom · Click the pin to land</div>

      <!-- Title screen — the arcade boot menu over the orbit view -->
      <div id="title-screen" class="hidden">
        <div class="ts-logo">PLANETFALL</div>
        <div class="ts-tag">THE REBELLION IS WAITING</div>

        <div id="ts-main" class="ts-menu">
          <button class="ts-item" type="button" data-action="start">START GAME</button>
          <button class="ts-item" type="button" data-action="leaderboard">LEADERBOARD</button>
          <button class="ts-item" type="button" data-action="options">OPTIONS</button>
        </div>

        <div id="ts-options" class="ts-menu hidden">
          <button class="ts-item" type="button" data-action="controls">CONTROLS</button>
          <button class="ts-item" type="button" data-action="sound">SOUND</button>
          <button class="ts-item" type="button" data-action="display">DISPLAY</button>
          <button class="ts-item" type="button" data-action="back">BACK</button>
        </div>

        <div id="ts-controls" class="ts-panel hidden">
          <div class="ts-group">
            <div class="ts-group-head">IN ORBIT</div>
            <div class="ts-ctrl"><span class="bf-key">drag</span> orbit the planet</div>
            <div class="ts-ctrl"><span class="bf-key">scroll</span> zoom</div>
            <div class="ts-ctrl"><span class="bf-key">click</span> the pin to land</div>
          </div>
          <div class="ts-group">
            <div class="ts-group-head">ON THE ISLAND</div>
            <div class="ts-ctrl"><span class="bf-keys"><span class="bf-key">W</span><span class="bf-key">A</span><span class="bf-key">S</span><span class="bf-key">D</span></span> move <span class="bf-dim">(or arrows)</span></div>
            <div class="ts-ctrl"><span class="bf-key">mouse</span> look around <span class="bf-dim">(click to capture)</span></div>
            <div class="ts-ctrl"><span class="bf-key">E</span> interact</div>
            <div class="ts-ctrl"><span class="bf-key">M</span> bird's-eye map</div>
            <div class="ts-ctrl"><span class="bf-key">B</span> return to orbit</div>
            <div class="ts-ctrl"><span class="bf-key">Esc</span> release the mouse / […]

> TOOL

tool_result
id: call_sxQcFfD7h3G01gcWbjeC8AKM
```
Chunk ID: fe0e4d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 7344
Output:
src/leaderboard.js:1:const API_PATH = "/api/leaderboard";
src/launchView.js:6:import { createLeaderboardEntry } from "./leaderboard.js";
src/launchView.js:7:import { createLeaderboardPanel } from "./leaderboardPanel.js";
src/launchView.js:355:  const leaderboardPanel = createLeaderboardPanel({ mount: hud, onClose: hideLeaderboard });
src/launchView.js:426:    outputEl.classList.remove("hidden");
src/launchView.js:431:    outputEl?.classList.add("hidden");
src/launchView.js:434:    answersEl?.classList.add("hidden");
src/launchView.js:450:    menuEl.classList.remove("hidden");
src/launchView.js:461:    answersEl.classList.remove("hidden");
src/launchView.js:512:    answersEl?.classList.add("hidden");
src/launchView.js:513:    menuEl?.classList.add("hidden");
src/launchView.js:534:      consoleEl?.classList.add("hidden");
src/launchView.js:543:    ignitionEl.classList.remove("hidden", "pop", "is-go");
src/launchView.js:557:    setTimeout(() => ignitionEl?.classList.add("hidden"), 1300);
src/launchView.js:626:    briefingEl?.classList.remove("hidden");
src/launchView.js:627:    consoleEl?.classList.add("hidden");
src/launchView.js:633:    briefingEl?.classList.add("hidden");
src/launchView.js:634:    consoleEl?.classList.remove("hidden");
src/launchView.js:649:    consoleEl?.classList.add("hidden");
src/launchView.js:650:    failEl?.classList.remove("hidden");
src/launchView.js:663:    ignitionEl?.classList.add("hidden");
src/launchView.js:686:    failEl?.classList.add("hidden");
src/launchView.js:687:    winEl?.classList.add("hidden");
src/launchView.js:688:    consoleEl?.classList.remove("hidden");
src/launchView.js:719:    briefingEl?.classList.add("hidden");
src/launchView.js:720:    consoleEl?.classList.add("hidden");
src/launchView.js:721:    failEl?.classList.add("hidden");
src/launchView.js:722:    ignitionEl?.classList.add("hidden");
src/launchView.js:725:    winEl?.classList.remove("hidden");
src/launchView.js:743:    hud?.classList.add("has-leaderboard");
src/launchView.js:744:    leaderboardPanel.show(run, {
src/launchView.js:749:    hud?.classList.remove("has-leaderboard");
src/launchView.js:750:    leaderboardPanel.hide();
src/launchView.js:766:      briefingEl?.classList.add("hidden");
src/launchView.js:767:      consoleEl?.classList.add("hidden");
src/launchView.js:768:      winEl?.classList.add("hidden");
src/launchView.js:769:      ignitionEl?.classList.add("hidden");
src/launchView.js:779:    if (leaderboardPanel.containsTarget(e.target)) return;
src/launchView.js:780:    if (leaderboardPanel.isVisible()) {
src/launchView.js:781:      leaderboardPanel.focusInput();
src/launchView.js:890:        winEl?.classList.remove("hidden");
src/launchView.js:905:    hud?.classList.remove("hidden");
src/launchView.js:909:      winEl?.classList.remove("hidden");
src/launchView.js:914:      consoleEl?.classList.remove("hidden");
src/launchView.js:926:    hud?.classList.add("hidden");
src/launchView.js:927:    briefingEl?.classList.add("hidden");
src/launchView.js:928:    consoleEl?.classList.add("hidden");
src/launchView.js:929:    ignitionEl?.classList.add("hidden");
src/launchView.js:931:    winEl?.classList.add("hidden");
src/launchView.js:932:    failEl?.classList.add("hidden");
src/islandView.js:8:import { createLeaderboardEntry } from "./leaderboard.js";
src/islandView.js:9:import { createLeaderboardPanel } from "./leaderboardPanel.js";
src/islandView.js:212:  const leaderboardPanel = createLeaderboardPanel({ mount: islandHud, onClose: hideLeaderboard });
src/islandView.js:256:    if (text) { promptEl.textContent = text; promptEl.classList.remove("hidden"); }
src/islandView.js:257:    else promptEl.classList.add("hidden");
src/islandView.js:263:    tutorialEl.classList.remove("hidden", "is-onboarding");
src/islandView.js:264:    if (ms > 0) tutorialTimer = setTimeout(() => tutorialEl.classList.add("hidden"), ms);
src/islandView.js:301:    tutorialEl?.classList.add("hidden");
src/islandView.js:304: […]

> AGENT

The existing panel already has the right states; this looks like a routing/bootstrap change, plus maybe a tiny panel tweak so Back can feel like “home” on the standalone page. I’m checking the CSS and Vite/Vercel config before editing so direct refreshes behave too.

> TOOL

tool_use exec_command
id: call_Oqf30M6OAD0SVdyKCSG9a4pg
```json
{
  "cmd": "sed -n '1,130p' src/style.css",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_use exec_command
id: call_DbeAUca3OCal2ZG3u0QwJMkU
```json
{
  "cmd": "sed -n '2980,3385p' src/style.css",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 26000
}
```

> TOOL

tool_use exec_command
id: call_C7s3DocHaFsweinrsdcACHzi
```json
{
  "cmd": "sed -n '1,220p' vite.config.js",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_zSdzsuoZ5B4FyHm3viZzbEjX
```json
{
  "cmd": "find . -maxdepth 3 -name 'vercel.json' -o -name '.openai' -o -name 'hosting.json' -o -name '*.json' | sort | sed -n '1,120p'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_TQw2EU03X7itDXyGAsjXFY4f
```json
{
  "cmd": "cat package.json",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_Oqf30M6OAD0SVdyKCSG9a4pg
```
Chunk ID: a53df6
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 718
Output:
:root {
  --accent: #6fe3ff;
  --accent-warm: #ffb86b;
  --ink: #e8f4ff;
  --panel-bg: rgba(8, 14, 26, 0.82);
  --pin-shell: #171126;
  --pin-rim: rgba(255, 244, 232, 0.96);
  --pin-core: #d79e3a;
  --pin-shadow: rgba(2, 4, 10, 0.72);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #02040a;
  color: var(--ink);
  font-family: "SF Mono", "JetBrains Mono", ui-monospace, Menlo, monospace;
  cursor: default;
}

#scene {
  position: fixed;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
}

#ui {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 10;
}

#hud {
  position: absolute;
  top: 28px;
  left: 32px;
}

.hud-title {
  font-size: 26px;
  letter-spacing: 0.42em;
  font-weight: 600;
  text-shadow: 0 0 18px rgba(111, 227, 255, 0.55);
}

#hint {
  position: absolute;
  bottom: 26px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  letter-spacing: 0.12em;
  opacity: 0.55;
  white-space: nowrap;
}

/* ---------- title screen (arcade boot menu) ---------- */

/* The orbit view keeps rendering behind it — only a soft vignette for
   legibility, so the planet stays the attract backdrop. */
#title-screen {
  position: absolute;
  inset: 0;
  z-index: 35;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: […]

> TOOL

tool_result
id: call_DbeAUca3OCal2ZG3u0QwJMkU
```
Chunk ID: 30af7d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2174
Output:
}

/* The ignition flash — one bright gold breath over everything */
#lc-flash {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 62%,
    rgba(255, 236, 190, 0.95), rgba(255, 210, 122, 0.55) 45%, rgba(255, 180, 90, 0) 75%);
  opacity: 0;
  pointer-events: none;
}
#lc-flash.show { animation: lc-flash 1.4s ease-out both; }
@keyframes lc-flash {
  0% { opacity: 0; }
  12% { opacity: 1; }
  100% { opacity: 0; }
}

/* Leaderboard overlay after run-ending moments. */
#island-hud.has-leaderboard #level-fail,
#db-hud.has-leaderboard #db-fail,
#lc-hud.has-leaderboard #lc-win,
#lc-hud.has-leaderboard #lc-fail {
  display: none;
}

.leaderboard {
  position: fixed;
  inset: 0;
  z-index: 38;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: clamp(30px, 7vh, 70px) clamp(18px, 7vw, 104px) 28px;
  pointer-events: auto;
  color: #fff;
  background:
    linear-gradient(180deg, rgba(19, 31, 46, 0.5), rgba(12, 16, 28, 0.62)),
    radial-gradient(ellipse at 50% 24%, rgba(111, 227, 255, 0.12), rgba(2, 4, 10, 0.58) 68%);
}
.leaderboard.hidden { display: none; }
.leaderboard.is-entry {
  justify-content: flex-start;
  padding-top: clamp(128px, 24vh, 260px);
}
.leaderboard.is-board { justify-content: flex-start; }

.lb-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  width: min(980px, 100%);
  margin-bottom: clamp(16px, 3vh, 30px);
  text-align: center;
}
.leaderboard.is-entry […]

> TOOL

tool_result
id: call_C7s3DocHaFsweinrsdcACHzi
```
Chunk ID: 7377e0
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 46
Output:
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    watch: {
      ignored: [
        "**/.vercel/**",
        "**/dist/**",
      ],
    },
  },
});

```

> TOOL

tool_result
id: call_zSdzsuoZ5B4FyHm3viZzbEjX
```
Chunk ID: beaace
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1590
Output:
./.claude/settings.json
./.codex/hooks.json
./.entire/settings.json
./.entire/settings.local.json
./.entire/tmp/pre-prompt-019ea07b-c533-7490-bc73-b418f6bcec4e.json
./.entire/tmp/pre-prompt-019ea8fa-feb1-7f93-ac74-4c3373a82d7f.json
./.entire/tmp/pre-prompt-019eae1a-0617-7291-abac-f438875870d4.json
./.entire/tmp/pre-prompt-019eb121-52c3-74e3-a296-e2cdce6fa2b5.json
./.entire/tmp/pre-prompt-019ec66b-5210-7711-a71e-86632c398f1f.json
./.entire/tmp/pre-prompt-019ecfb7-79f9-7263-bf8c-1f3b136a6a3c.json
./.entire/tmp/pre-prompt-019ed0b0-ee61-7341-8509-df97a795155d.json
./.entire/tmp/pre-prompt-019ed0f2-4373-7820-a3b8-d51bac5e7d6d.json
./.entire/tmp/pre-prompt-019ed1e2-c216-7cf1-b680-035524a8fc09.json
./.entire/tmp/pre-prompt-019ed2c0-e620-7ab0-bafc-6ea27adb45c9.json
./.entire/tmp/pre-prompt-019ed2e2-c0ba-7551-9a3b-dcad81973311.json
./.entire/tmp/pre-prompt-019ed44c-d791-7742-8652-f4d3af4f45f1.json
./.entire/tmp/pre-prompt-019ed44e-4be8-7c33-a28c-229573f5ad26.json
./.entire/tmp/pre-prompt-019ed688-f0d8-7531-a5f3-ca1cf17f7c75.json
./.entire/tmp/pre-prompt-019ed6d6-ef92-7bc1-91e1-eb148c3140a6.json
./.entire/tmp/pre-prompt-019ed6d8-372d-7b72-ab4c-3532dd77b3e4.json
./.entire/tmp/pre-prompt-019ed6ed-d8b6-7d40-b672-764045f61e13.json
./.entire/tmp/pre-prompt-019ed7a6-b622-7683-a718-e3f4947d2fac.json
./.entire/tmp/pre-prompt-019ed7bd-1336-7123-ad87-5b5a67325237.json
./.entire/tmp/pre-prompt-019ed7c2-0e29-7b52-b92a-ff8e6f9573a0.json
./.entire/tmp/pre-prompt-019ed8f8-438a-7e70-95ce-59a9cadd7a34.json
./.entire/tmp/pre-prompt-019ed902-832b-70a3-9eea-2e70d234573b.json
./.entire/tmp/pre-prompt-019ed92d-fcab-7bc0-9f52-222f86167dc5.json
./.entire/tmp/pre-prompt-019ed942-4ed9-7c21-860b-c4e15f3b0e85.json
./.entire/tmp/pre-prompt-019ed94d-c6f3-7661-a59e-7d86b90bce9f.json
./.entire/tmp/pre-prompt-019ed95a-540c-72b3-acb9-7d481f967116.json
./.entire/tmp/pre-prompt-019ed974-19ee-72c2-b4c7-407a029544b2.json
./.entire/tmp/pre-prompt-019ed992-2382-7801-9bed-79c4b9980845.json
./.entire/tmp/pre-prompt-019edb14-5c03-7b62-9c55-5fd2ea99a5c6.json
./.entire/tmp/pre-prompt-019edb14-9a44-7081-bc6e-c597e4807a42.json
./.entire/tmp/pre-prompt-019edb22-0a24-74a1-922d-1f66ae0d7b88.json
./.entire/tmp/pre-prompt-019edb4e-76f5-7800-be12-ffff1334f57b.json
./.entire/tmp/pre-prompt-019edb59-c141-7680-9a9d-6d5e46df37a4.json
./.entire/tmp/pre-prompt-019edf9f-acdb-7840-b8f9-88f544de7883.json
./.entire/tmp/pre-prompt-019edfaf-d18c-73d0-b7dc-f2d91b48d0e1.json
./.entire/tmp/pre-prompt-019edfb1-47e4-7933-acbc-2c230b84fe33.json
./.entire/tmp/pre-prompt-019edfb7-5b5b-7d23-9883-c5446a3823b8.json
./.entire/tmp/pre-prompt-019ee092-5d6c-7481-b301-b1d6cd77de0e.json
./.entire/tmp/pre-prompt-019ee09f-d2c6-72b1-94dd-f0863fe8464a.json
./.entire/tmp/pre-prompt-47f1677e-c6c9-4dba-8e3f-1e3dfe715b26.json
./.entire/tmp/pre-prompt-592fcac1-50f9-42cf-ba16-981946751465.json
./.entire/tmp/pre-prompt-b6016fa9-6201-4415-9479-206ca1bfa2d0.json
./.entire/tmp/pre-prompt-d3afb3b6-26e5-47d2-8194-cdab6e068364.json
./.entire/tmp/pre-prompt-eb4f7ed1-9c0a-467a-93fd-61a231e8856e.json
./.entire/tmp/pre-prompt-fab2dc1a-be50-469b-af6c-6ab439a096e1.json
./.git/entire-sessions/019ec66b-5210-7711-a71e-86632c398f1f.json
./.git/entire-sessions/019ecfb7-79f9-7263-bf8c-1f3b136a6a3c.json
./.git/entire-sessions/019ed0b0-ee61-7341-8509-df97a795155d.json
./.git/entire-sessions/019ed0f2-4373-7820-a3b8-d51bac5e7d6d.json
./.git/entire-sessions/019ed1e2-c216-7cf1-b680-035524a8fc09.json
./.git/entire-sessions/019ed2c0-e620-7ab0-bafc-6ea27adb45c9.json
./.git/entire-sessions/019ed2e2-c0ba-7551-9a3b-dcad81973311.json
./.git/entire-sessions/019ed44c-d791-7742-8652-f4d3af4f45f1.json
./.git/entire-sessions/019ed44e-4be8-7c33-a28c-229573f5ad26.json
./.git/entire-sessions/019ed688-f0d8-7531-a5f3-ca1cf17f7c75.json
./.git/entire-sessions/019ed6d6-ef92-7bc1-91e1-eb148c3140a6.json
./.git/entire-sessions/019ed6d8-372d-7b72-ab4c-3532dd77b3e4.json
./.git/entire-sessions/019ed6ed-d8b6-7d40-b672-764045f61e13.json
./.git/entire-sessions/019ed7a6-b622-7683-a718-e3f4947d2fac.json
./.git/entire-sessions/019ed7bd-1336-7123-ad87-5b5a67325237.json
./.git/entire-sessions/019ed7c2-0e29-7b52-b92a-ff8e6f9573a0.json
./.git/entire-sessions/019ed8f8-438a-7e70-95ce-59a9cadd7a34.json
./.git/entire-sessions/019ed902-832b-70a3-9eea-2e70d234573b.json
./.git/entire-sessions/019ed92d-fcab-7bc0-9f52-222f86167dc5.json
./.git/entire-sessions/019ed942-4ed9-7c21-860b-c4e15f3b0e85.json
./.git/entire-sessions/019ed94d-c6f3-7661-a59e-7d86b90bce9f.json
./.git/entire-sessions/019ed95a-540c-72b3-acb9-7d481f967116.json
./.git/entire-sessions/019ed974-19ee-72c2-b4c7-407a029544b2.json
./.git/entire-sessions/019ed992-2382-7801-9bed-79c4b9980845.json
./.git/entire-sessions/019edb14-5c03-7b62-9c55-5fd2ea99a5c6.json
./.git/entire-sessions/019edb14-9a44-7081-bc6e-c597e4807a42.json
./.git/entire-sessions/019edb22-0a24-74a1-922d-1f66ae0d7b88.json
./.git/entire-sessions/019edb4e-76f5-7800-be12-ffff1334f57b.json
./.git/entire-sessions/019edb59-c141-7680-9a9d-6d5e46df37a4.json
./.git/entire-sessions/019edf9f-acdb-7840-b8f9-88f544de7883.json
./.git/entire-sessions/019edfaf-d18c-73d0-b7dc-f2d91b48d0e1.json
./.git/entire-sessions/019edfb1-47e4-7933-acbc-2c230b84fe33.json
./.git/entire-sessions/019edfb7-5b5b-7d23-9883-c5446a3823b8.json
./.git/entire-sessions/019ee092-5d6c-7481-b301-b1d6cd77de0e.json
./.git/entire-sessions/019ee09f-d2c6-72b1-94dd-f0863fe8464a.json
./.git/entire-sessions/233712ad-9679-40e0-bc3a-3cafadc74605.json
./.git/entire-sessions/38573ee1-23f1-46a2-a4f2-13ba6a15bf0c.json
./.git/entire-sessions/3b5a9bec-34c4-48d5-9502-dd21f9e1e011.json
./.git/entire-sessions/47f1677e-c6c9-4dba-8e3f-1e3dfe715b26.json
./.git/entire-sessions/88508f41-9260-4ba2-ba37-2ae5c118c0fa.json
./.git/entire-sessions/b4204c32-77ab-409a-9627-b677ca8be616.json
./.git/entire-sessions/ed80b65d-9ba6-42c1-bcf1-89ed4c4519f3.json
./.vercel/node/package-manifest.json
./.vercel/output/builds.json
./.vercel/output/config.json
./.vercel/project.json
./node_modules/.package-lock.json
./node_modules/esbuild/package.json
./node_modules/fsevents/package.json
./node_modules/nanoid/package.json
./node_modules/picocolors/package.json
./node_modules/postcss/package.json
./node_modules/rollup/package.json
./node_modules/source-map-js/package.json
./node_modules/three/package.json
./node_modules/vite/package.json
./package-lock.json
./package.json

```

> TOOL

tool_result
id: call_TQw2EU03X7itDXyGAsjXFY4f
```
Chunk ID: 518e4a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 147
Output:
{
  "name": "planetfall",
  "version": "0.0.1",
  "private": true,
  "license": "GPL-3.0-only",
  "type": "module",
  "description": "Planetfall — a stranded astronaut reconstructs a lost ship's memory by recovering context. 3D world prototype.",
  "scripts": {
    "dev": "vite",
    "dev:vercel": "VITE_USE_REMOTE_LEADERBOARD=1 npx vercel@latest dev",
    "test": "node --test",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.4.10"
  },
  "dependencies": {
    "@neondatabase/serverless": "^1.1.0",
    "three": "^0.169.0"
  }
}

```

> AGENT

Direct client-side detection solves Vite dev, but production direct refreshes may need a rewrite too. I’m going to add source config for `/leaderboard` to serve the SPA entry, then patch the app boot path to open the existing leaderboard board on that path.

> AGENT

I’m editing `main.js` and adding a tiny Vercel rewrite config now. The code path will treat `/leaderboard` as a first-class boot mode, not as a query-string dev shortcut.

> AGENT

The boot path is patched; I’m adding the matching CSS so the standalone leaderboard has the same clean overlay behavior as the title-menu leaderboard.

> AGENT

The implementation is in place. I’m checking the diff, then I’ll run the existing test/build suite and a local server pass against `/leaderboard`.

> TOOL

tool_use exec_command
id: call_tplbWtgL1vYTjGjx5VYPVU5G
```json
{
  "cmd": "git diff -- src/main.js src/style.css vercel.json",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_BvQphwQjNMYVU8MSKbR9Ml1t
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_tplbWtgL1vYTjGjx5VYPVU5G
```
Chunk ID: 582037
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 537
Output:
diff --git a/src/main.js b/src/main.js
index bfce42d..a606ca4 100644
--- a/src/main.js
+++ b/src/main.js
@@ -114,6 +114,8 @@ if (bgm && audioPanel && audioToggle && audioMute && audioVolume) {
 
 const params = new URLSearchParams(location.search);
 const requestedView = params.get("view");
+const normalizedPath = location.pathname.replace(/\/+$/, "") || "/";
+const isLeaderboardRoute = normalizedPath === "/leaderboard";
 
 function normalizeEndOutcome(value) {
   const v = String(value || "").trim().toLowerCase();
@@ -163,6 +165,7 @@ let level2Done = jumpToLevel3;
 
 function startNewGame() {
   const cleanUrl = new URL(window.location.href);
+  cleanUrl.pathname = "/";
   cleanUrl.search = "";
   cleanUrl.hash = "";
   window.location.assign(cleanUrl.href);
@@ -231,6 +234,10 @@ const titleLeaderboardPanel = createLeaderboardPanel({
 function closeTitleLeaderboard() {
   titleLeaderboardRequest += 1;
   titleLeaderboardPanel.hide();
+  if (isLeaderboardRoute) {
+    startNewGame();
+    return;
+  }
   const resume = resumeTitleAfterLeaderboard;
   resumeTitleAfterLeaderboard = null;
   resume?.();
@@ -268,7 +275,12 @@ const titleScreen = createTitleScreen({
   },
   onStart: () => planetView.setLandingMarkerHold(false),
 });
-if (!requestedView && !params.get("level") && !endShortcut) titleScreen.show();
+if (isLeaderboardRoute) {
+  document.body.classList.add("leaderboard-route");
+  showTitleLeaderboard();
+} else if (!requestedView && !params.get("level") && !endShortcut) {
+  titleScreen.show();
+}
 
 // ---------- fade transition ----------
 const fade = document.getElementById("fade");
diff --git a/src/style.css b/src/style.css
index 09b0a2a..62f9e85 100644
--- a/src/style.css
+++ b/src/style.css
@@ -98,6 […]

> TOOL

tool_result
id: call_BvQphwQjNMYVU8MSKbR9Ml1t
```
Chunk ID: dd9c61
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 30
Output:
## codex/leaderboard-route...origin/codex/leaderboard-route
 M src/main.js
 M src/style.css
?? .codex/
?? vercel.json

```

> AGENT

The diff is small and scoped. One nuance: `vercel.json` is new, so I’ll verify its contents separately while the tests and production build run.

> TOOL

tool_use exec_command
id: call_f2gqgtrjZdTvkVjijJcz8emt
```json
{
  "cmd": "npm test",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_2grI2bbWG7IXFVAm9EgeIAMx
```json
{
  "cmd": "npm run build",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_sfbVFPCgdICjeRhuHlJyuI8s
```json
{
  "cmd": "cat vercel.json",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_f2gqgtrjZdTvkVjijJcz8emt
```
Chunk ID: 9f9061
Wall time: 0.2636 seconds
Process exited with code 0
Original token count: 308
Output:

> planetfall@0.0.1 test
> node --test

TAP version 13
# Subtest: normalizes username identity case-insensitively and trims repeated spaces
ok 1 - normalizes username identity case-insensitively and trims repeated spaces
  ---
  duration_ms: 0.5115
  type: 'test'
  ...
# Subtest: does not replace a personal best with a lower score
ok 2 - does not replace a personal best with a lower score
  ---
  duration_ms: 0.082917
  type: 'test'
  ...
# Subtest: replaces a personal best with a higher score
ok 3 - replaces a personal best with a higher score
  ---
  duration_ms: 0.042375
  type: 'test'
  ...
# Subtest: uses level and completion as score tie-breakers
ok 4 - uses level and completion as score tie-breakers
  ---
  duration_ms: 0.047583
  type: 'test'
  ...
# Subtest: uses progress, time remaining, and duration as later tie-breakers
ok 5 - uses progress, time remaining, and duration as later tie-breakers
  ---
  duration_ms: 0.31225
  type: 'test'
  ...
# Subtest: does not replace an exactly tied personal best
ok 6 - does not replace an exactly tied personal best
  ---
  duration_ms: 0.055667
  type: 'test'
  ...
1..6
# tests 6 […]

> TOOL

tool_result
id: call_2grI2bbWG7IXFVAm9EgeIAMx
```
Chunk ID: 2ff5ce
Wall time: 0.8940 seconds
Process exited with code 0
Original token count: 176
Output:

> planetfall@0.0.1 build
> vite build

vite v5.4.21 building for production...
transforming...
✓ 28 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                  21.45 kB │ gzip:   5.02 kB
dist/assets/index-Bqs6SScf.css   59.59 kB │ gzip:  12.42 kB
dist/assets/index-D997r4Gk.js   658.55 kB │ gzip: 178.51 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 537ms

```

> TOOL

tool_result
id: call_sfbVFPCgdICjeRhuHlJyuI8s
```
Chunk ID: dab5ee
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 33
Output:
{
  "rewrites": [
    { "source": "/leaderboard", "destination": "/" },
    { "source": "/leaderboard/", "destination": "/" }
  ]
}

```

> AGENT

Tests and build pass; Vite emitted only its existing large-chunk warning. I’m starting a local dev server now and will hit `/leaderboard` directly to make sure the route serves and boots cleanly.

> TOOL

tool_use exec_command
id: call_7S565mkzQqoOFPpUXn2jfsf4
```json
{
  "cmd": "npm run dev -- --host 127.0.0.1 --port 5173",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000,
  "tty": true
}
```

> TOOL

tool_result
id: call_7S565mkzQqoOFPpUXn2jfsf4
```
Chunk ID: dd14f0
Wall time: 1.0017 seconds
Process running with session ID 65391
Original token count: 59
Output:

> planetfall@0.0.1 dev
> vite --host 127.0.0.1 --port 5173
























[1;1H[0J
  VITE v5.4.21  ready in 91 ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  press h + enter to show help

```

> AGENT

The dev server is up at `http://127.0.0.1:5173/`. I’m going one step past curl and loading it in a browser so runtime errors or blank overlays don’t slip through.

> AGENT

The browser connector isn’t available in this thread, so I’m checking whether the local Node runtime has Playwright available; if not, I’ll still validate the route via HTTP and the production build.

> TOOL

tool_use js
id: call_gU85Mq7Adr5YkP5ig4yNSGD8
```json
{
  "title": "Check Playwright availability",
  "code": "try {\n  await import('playwright');\n  nodeRepl.write('playwright:available');\n} catch (error) {\n  nodeRepl.write(`playwright:missing:${error.code || error.message}`);\n}"
}
```

> TOOL

tool_result
id: call_gU85Mq7Adr5YkP5ig4yNSGD8
```
Wall time: 0.3779 seconds
Output:
[{"type":"text","text":"playwright:available"}]
```

> AGENT

Playwright is available, so I’m loading the live `/leaderboard` page headlessly and checking the DOM plus console errors. This should catch the actual boot behavior, not just whether files compile.

> TOOL

tool_use js
id: call_V4Ly4ZWCyJFWpPYVRkVf4mcj
```json
{
  "title": "Verify /leaderboard route",
  "timeout_ms": 60000,
  "code": "var playwrightMod = await import('playwright');\nvar chromiumBrowser = await playwrightMod.chromium.launch({ headless: true });\nvar leaderboardPage = await chromiumBrowser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });\nvar consoleErrors = [];\nvar pageErrors = [];\nleaderboardPage.on('console', (message) => {\n  if (message.type() === 'error') consoleErrors.push(message.text());\n});\nleaderboardPage.on('pageerror', (error) => pageErrors.push(error.message));\nawait leaderboardPage.goto('http://127.0.0.1:5173/leaderboard', { waitUntil: 'domcontentloaded' });\nawait leaderboardPage.waitForSelector('.leaderboard.is-board:not(.hidden)', { timeout: 10000 });\nawait leaderboardPage.waitForTimeout(500);\nvar routeState = await leaderboardPage.evaluate(() => ({\n  pathname: window.location.pathname,\n  bodyClass: document.body.className,\n  panelVisible: !!document.querySelector('.leaderboard.is-board:not(.hidden)'),\n  title: document.querySelector('[data-lb-title]')?.textContent || '',\n  label: document.querySelector('.lb-board-label')?.textContent || '',\n  emptyText: document.querySelector('.lb-empty')?.textContent || '',\n  backText: document.querySelector('[data-lb-back]')?.textContent || '',\n  titleScreenVisible: !document.getElementById('title-screen')?.classList.contains('hidden'),\n  hudDisplay: getComputedStyle(document.getElementById('hud')).display,\n  hintDisplay: getComputedStyle(document.getElementById('hint')).display,\n  audioDisplay: getComputedStyle(document.getElementById('audio-panel')).display,\n}));\nvar png = await leaderboardPage.screenshot({ fullPage: true });\nawait chromiumBrowser.close();\nawait nodeRepl.emitImage({ bytes: png, mimeType: 'image/png' });\nnodeRepl.write(JSON.stringify({ routeState, consoleErrors, pageErrors }, null, 2));"
}
```

> TOOL

tool_result
id: call_V4Ly4ZWCyJFWpPYVRkVf4mcj
```
Wall time: 0.0270 seconds
Output:
[{"type":"text","text":"browserType.launch: Executable doesn't exist at /home/<USER>/Library/Caches/ms-playwright/chromium_headless_shell-1200/chrome-headless-shell-mac-arm64/chrome-headless-shell\n╔═════════════════════════════════════════════════════════════════════════╗\n║ Looks like Playwright Test or Playwright was just installed or updated. ║\n║ Please run the following command to download new browsers:              ║\n║                                                                         ║\n║     npx playwright install                                              ║\n║                                                                         ║\n║ <3 Playwright Team                                                      ║\n╚═════════════════════════════════════════════════════════════════════════╝"}]
```

> AGENT

Playwright is installed but its bundled browser binary is missing. I’m checking for an existing system Chrome/Chromium first so we can avoid downloading a browser just for this verification pass.

> TOOL

tool_use exec_command
id: call_TkvjtkMLWIjysKTCunNzYRoT
```json
{
  "cmd": "ls /Applications | rg -i 'chrome|chromium|edge|brave|firefox|safari'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_H69nCSicdMGuXtHwMCAhp3oL
```json
{
  "cmd": "which google-chrome chromium chromium-browser chrome 2>/dev/null || true",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_Tv4hMYsRokdS13RefaraNfU2
```json
{
  "cmd": "curl -i http://127.0.0.1:5173/leaderboard | sed -n '1,40p'",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_TkvjtkMLWIjysKTCunNzYRoT
```
Chunk ID: 517f27
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 8
Output:
Google Chrome.app
Safari.app

```

> TOOL

tool_result
id: call_H69nCSicdMGuXtHwMCAhp3oL
```
Chunk ID: a3ac66
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 22
Output:
google-chrome not found
chromium not found
chromium-browser not found
chrome not found

```

> TOOL

tool_result
id: call_Tv4hMYsRokdS13RefaraNfU2
```
Chunk ID: 13f39f
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 409
Output:
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 21537  100 21537    0     0   865k      0 --:--:-- --:--:-- --:--:--  956k
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
Etag: W/"REDACTED"
Date: Fri, 19 Jun 2026 18:55:33 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 21537

<!DOCTYPE html>
<html lang="en">
  <head>
    <script type="module" src="/@vite/client"></script>

    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Planetfall</title>
    <link rel="stylesheet" href="/src/style.css" />
  </head>
  <body>
    <canvas id="scene"></canvas>

    <div id="ui">
      <header id="hud">
        <div class="hud-title">PLANETFALL</div>
      </header>

      <div id="hint">Drag to orbit · Scroll to zoom · Click the pin to land</div>

      <!-- Title screen — the arcade boot menu over the orbit view -->
      <div id="title-screen" class="hidden">
        <div class="ts-logo">PLANETFALL</div>
        <div class="ts-tag">THE REBELLION IS WAITING</div>

        <div id="ts-main" class="ts-menu">
          <button class="ts-item" type="button" data-action="start">START GAME</button>
          <button class="ts-item" type="button" data-action="leaderboard">LEADERBOARD</button>
          <button class="ts-item" type="button" data-action="options">OPTIONS</button>
        </div>

```

> AGENT

System Chrome is installed, and the HTTP route returns the SPA HTML. I’m re-running the browser verification against that Chrome executable now.

> TOOL

tool_use js
id: call_wN4MKeY9LYtv6t2jSnUeH3pK
```json
{
  "title": "Verify /leaderboard in Chrome",
  "timeout_ms": 60000,
  "code": "var playwrightMod2 = await import('playwright');\nvar systemChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';\nvar chromeBrowser = await playwrightMod2.chromium.launch({ headless: true, executablePath: systemChromePath });\nvar chromePage = await chromeBrowser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });\nvar consoleErrors2 = [];\nvar pageErrors2 = [];\nchromePage.on('console', (message) => {\n  if (message.type() === 'error') consoleErrors2.push(message.text());\n});\nchromePage.on('pageerror', (error) => pageErrors2.push(error.message));\nawait chromePage.goto('http://127.0.0.1:5173/leaderboard', { waitUntil: 'domcontentloaded' });\nawait chromePage.waitForSelector('.leaderboard.is-board:not(.hidden)', { timeout: 10000 });\nawait chromePage.waitForTimeout(500);\nvar routeState2 = await chromePage.evaluate(() => ({\n  pathname: window.location.pathname,\n  bodyClass: document.body.className,\n  panelVisible: !!document.querySelector('.leaderboard.is-board:not(.hidden)'),\n  title: document.querySelector('[data-lb-title]')?.textContent || '',\n  label: document.querySelector('.lb-board-label')?.textContent || '',\n  emptyText: document.querySelector('.lb-empty')?.textContent || '',\n  backText: document.querySelector('[data-lb-back]')?.textContent || '',\n  titleScreenVisible: !document.getElementById('title-screen')?.classList.contains('hidden'),\n  hudDisplay: getComputedStyle(document.getElementById('hud')).display,\n  hintDisplay: getComputedStyle(document.getElementById('hint')).display,\n  audioDisplay: getComputedStyle(document.getElementById('audio-panel')).display,\n}));\nvar screenshotPng2 = await chromePage.screenshot({ fullPage: true });\nawait chromeBrowser.close();\nawait nodeRepl.emitImage({ bytes: screenshotPng2, mimeType: 'image/png' });\nnodeRepl.write(JSON.stringify({ routeState: routeState2, consoleErrors: consoleErrors2, pageErrors: pageErrors2 }, null, 2));"
}
```

> TOOL

tool_result
id: call_wN4MKeY9LYtv6t2jSnUeH3pK
```
{
  "type": "input_text",
  "text": "Wall time: 6.3128 seconds\nOutput:"
}
{
  "type": "input_text",
  "text": "{\n  \"routeState\": {\n    \"pathname\": \"/leaderboard\",\n    \"bodyClass\": \"tv-on leaderboard-route\",\n    \"panelVisible\": true,\n    \"title\": \"Leaderboard\",\n    \"label\": \"Top 10 overall\",\n    \"emptyText\": \"Leaderboard unavailable\",\n    \"backText\": \"Back\",\n    \"titleScreenVisible\": false,\n    \"hudDisplay\": \"none\",\n    \"hintDisplay\": \"none\",\n    \"audioDisplay\": \"none\"\n  },\n  \"consoleErrors\": [\n    \"Failed to load resource: the server responded with a status of 404 (Not Found)\"\n  ],\n  \"pageErrors\": []\n}"
}
{
  "type": "input_image",
  "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAALQCAIAAABAH0oBAAAQAElEQVR4nOy9B6BmSVUnfuq+3K/REDACTED/REDACTED/fvG79b+3qk7VOVWn6tb93msYdr3Tc/rX9d1b4eSqul99s/OL+0EBaAjUXgFHH+8wVaC0o/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/RTY0SZr+yd7d5dqHw/MsuMY5/REDACTED/hbGLPoeqzo7powvqFEsLWyXaoJCozxn2h/Gknd7Oy+Xo9B/l/REDACTED/REDACTED/NvGYN4trhz4tS8Zfxc6pptbeR/N/REDACTED/x3/atmMoPJv0p/xXbsd9B/ovyPflXLADfuCyl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/M7wLUjTX1RNU19YEK17FHLPlnEeT/REDACTED/REDACTED/REDACTED/cW2bEUx/REDACTED/REDACTED/REDACTED/8z3/REDACTED/REDACTED/REDACTED/ZLHpaI/xhwFOCqZ9y5X/B67n20nCZZ3ZgTFOaRGa54eZUD+d/REDACTED/qqcG8fq4ODo/REDACTED/REDACTED/REDACTED/wE/REDACTED/ZzG7LmDnfAvrLGzxOvTDLkgpbCphw/oz4Plzcs2uPEDOOF/2ZGmxxOXBwKKWf/oIGZ6uoA/REDACTED/Wf7PFGWKGec1yWKdf/REDACTED/REDACTED/B8U12kaqVINSrVNexb0Y1FXq/REDACTED/LgFrhhlHIObIPZHC+HK9E/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/E2ou8UtOQImbIx2yjVM+xBollg/REDACTED/REDACTED/pwkPpxsORbLRex1clJ+RTb2Cdq/REDACTED/jcElDKcB+Moy+j01LY/REDACTED/REDACTED/VWnJSKazvdQdP4FsaFFsZWJH7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/4AMOmoPddqX8jdud8kYpxxpdS3xsw+mfqqwWv3n/REDACTED/F/REDACTED/16rUBS8K6ioYeZIatcKCE8JJjxh/REDACTED/REDACTED/REDACTED//3Yqx6NknzBCT5jP0TXjGqko0/iQlNEDAvjyofe0nrewM/V8CWlZT/LXtpot2IVw/xTeO7VrUNmdolpRpwc/REDACTED/REDACTED/REDACTED/9bSSLEqY/g5wGAdhVp4NZbNsFNOfEjsHXZu9U/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/avYPC+KYl7ARO1KlNsfnjQ642r/QRToXWOQZnACjfEoUa6mE/REDACTED/+pLCWxxo5Na4xWIU4h9h3RWrN/REDACTED/AVE90OQDAYeiGON0Dn0I9xuEb2Iural/ECdshNr+KN43iPqJbWLNvv/REDACTED/REDACTED/REDACTED/REDACTED/T+YZL4jUnGtzD/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ZS7DBQZdAbXwaXtX4HOf3irwNtDToki/REDACTED/REDACTED/REDACTED/MW0iXtNk4mM0ca6J2KV/HRHM8LImd3FpjmwYJF/REDACTED/REDACTED/REDACTED/kfoTZMf/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/I3/gEjC7YcbMT8kDI5Ich/2Q2GOtwKb/REDACTED/REDACTED/REDACTED/REDACTED/RcTUJG2wdb88qPW1DYZZ3UVBs/9yFcI/R/yP1ryXaRSjhUIPjB/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ugMFobhGFCLv67f++53xqRTa/REDACTED/REDACTED/yCF0qf2/B/REDACTED/E25CdtGv491UH/n8YL7KeN1y7LYTGdTwK9/REDACTED/REDACTED/V1cuyUW08/T5T1mVD3v9F/REDACTED/+cfjZE/REDACTED/REDACTED/xlOxx4SvRw/eTnl/3RyTMuJngzoFcGQrO/REDACTED/REDACTED/J+YJttwPQgrCSqZsCs7N1/PQT6u8ivC8KJtBRTrD8jGpb/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ZXph8Eb/29bnb7V+XsyKuVMr4WE/U+lctoPj/REDACTED/REDACTED/REDACTED/auEjLfiOlZR/FvHL+qhrRdLL2mMiO+/REDACTED/REDACTED/REDACTED/VjU2hQmrQnt/REDACTED/b/REDACTED/qK3IwzqqA3Y1ezYFE1VE8BHWI/REDACTED/REDACTED/REDACTED/eCREngm4AWa/REDACTED/Up//jUSLGx1WXt1Ogi6+EcDLkW/REDACTED/dP0OYN1suKu6c5A/pW5L4UOpHpI9BOS8jH67107SPZVY4+J/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/aV2E+4prTQLsckkI9LrBkVdaxS37R/REDACTED/Pu3dyVdwM+YSUf/REDACTED/ece865H/REDACTED/REDACTED/TT5SRstWg3kRcJVZ7i5/REDACTED/DV0HfnP2W9C2zeGo7Z/REDACTED/REDACTED/UcHCaZEdIZ/REDACTED/REDACTED/JIlCblgX8Rfsu7lSOY9Ddbu8K/REDACTED/REDACTED/REDACTED/W/REDACTED/REDACTED/REDACTED/REDACTED/Jcj2GQ5omm/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/94vAPMYRRy6qihHqe2rWA6Dyl2iCo/REDACTED/C+ywPRYnddLkfcbEj/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QVa7aVCsLw8+aQfK6Y5Hrpw78S9eeU0/REDACTED/REDACTED/REDACTED/aGmKWJ2XXXC9wLD3kT4dd4U2p3P47mN3Z/REDACTED/REDACTED/REDACTED/CwHaWKf/REDACTED/Im7NfogGcsIP4a8hVx58J88/tZNPoPfbiU/REDACTED/REDACTED/REDACTED/REDACTED/aY2ZBhxyQU/p5niE/REDACTED/zOQ7pP9IzzvvnHPOOfu9773siz6ipJ/l/t9zcE3/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/SpcvZa5mmMaIdOK162lSmUg+Ha8vF5WmSmMGOR/FR4KqVJuJW0Z/7KtvsFAtMO5u/DbGknHPGucEUSiFWui19HpZv/REDACTED/Otvv/jBd/REDACTED/T+SNYYHncp01v/U63B81Qt9qDCnDQ/REDACTED/REDACTED/qnzWEdYU2wEaQcd45iacROK/REDACTED/REDACTED/2vpZ4hpTnGX5mh05o6U/REDACTED/aG7dEB9v1Ch9hLWKR6v9DsI7GS8u/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nTOCAmOqa6jmt/REDACTED/REDACTED/IYOi/REDACTED/oPZSKshM3h5rSRlFGB+4Rmp/REDACTED/UvhZA40X1CwGZUUwX+ySM8ZTGWRJ/REDACTED/REDACTED/REDACTED/KXzhtWWmXQ/zRWlm2qxh51/REDACTED/REDACTED/ufVWqe/REDACTED/9kQbCI0S5im3W+rs34w7YCi0H6/REDACTED/REDACTED/REDACTED/5+YEgmIj/Tl7SYcAdcN9kYwk3d/VbqIq68H7VHCT+HyXB0fx0e8qpfQhzHHUBe/REDACTED/REDACTED/REDACTED/REDACTED/Uhl9y/REDACTED/REDACTED/REDACTED/DYJ/REDACTED/+gk+hhhxe5QV2kU1y6hmoBezVkWI/REDACTED/REDACTED/REDACTED/8G5NRTjO85NdYuReq2OVSWLBCFp/REDACTED/REDACTED/pbgwZ2TMs7S/iZ7CIo7iLP1h2/REDACTED/5JfO4ck2cKbOL+GV4z/REDACTED/REDACTED/83oi5n4+PxzOJD3FYUcUiG1Ckt/REDACTED/REDACTED/REDACTED/4/REDACTED/JlPFXmrZIHNuOHJle2b/pvI87CMEWhvpW7xNiGn8HWJ5ciRQ7YQVQke/REDACTED/REDACTED/REDACTED/REDACTED/gQke7QFeZ+Fe1GLBD6o6D0Gz7+nkz/REDACTED/REDACTED//REDACTED/lVaxH0VNVudyT093vWeVp/wfGC5w/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/6nOt405/CC1l1qa7ipTXJ+nFQYf7iwkf4m/REDACTED/gMlicuMY23pIcYzLGJwgsgSHuA/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/y++4A0Q63Klqp6yDDXf/REDACTED/REDACTED/YEmrSfmHLJkmpg04WjOTySc7FV/REDACTED/REDACTED/REDACTED/DpeHyOkjoJ38BN/REDACTED/udcoW8heUzNM/Ru/fu27dv79GjR4/dfXec/REDACTED/REDACTED/REDACTED/+ML+RV/REDACTED/REDACTED/OZX3vRhRfwinpyYuXEr/REDACTED//5W3veNe/vm9uYbnf2EydBXai33ZeP3HxBY9/1jO/AfLX7/zu7x8+ujK3tFzee2/X1jbWjv/QD3zPgx/REDACTED/ryi/Qk+PCT3lbK+/tOf+eM//YvFpT3N4lJ3YzuZbKwefdiDHvC93/tdMHQdO3b8tltv/cJtt91y8xduuvmWm266qcXfv17YtWdueU+/VZjwq+vfxsrd87PqD/7773S7rYOtdMPvNO3Y8eOHDx++7PIrrrzy/REDACTED/fZyf/vndbm5s33Hjj61//d//zf/3V6urq3OLSwvIpRjRjbLZb1llduffBU/7Tf/rxwtDe+KZLr/rANd2SjZqdJ44YIr3tdmW7fj/REDACTED/Ymh+7q2cnlIJ/jN1RM/REDACTED/REDACTED/REDACTED/aU22YyA0tf/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/591zv/+X73uy8QW/REDACTED/6TV/REDACTED/e73/6gB9xfNjlzveIVf/ybv/W7u/YenF1cSjXD0xOHb59sbVx/7b/vWl5WA/J1z3WTms99/oZLLrn0VX/REDACTED/E//gSqrmHlWFtbPe9+D2lm5/ccOL0r2Fw9fuLokd/7vd95/nd8u+CXinjStjfWp1PmAAAQAElEQVTc8Pl//df3/dWrX/Pxj3+i06LlfafOLCxGetttMx6785bHPPor//Gtb65TXzqW3oPddeSuT3zik7/6a7/xoQ9/REDACTED/0u3z7n74OnmXeKsd4hqaddOrBw9/LJf/2/f933fw/oRbur/+ujH/v3rvv5Z87t2L3a6SvWTT5DWjh/pptOXX/REDACTED/jSzM4t7z2gZ2aTL0jo1SN3djr8iY9/REDACTED/REDACTED/H4tk0jutV/REDACTED/REDACTED/A7DwwX5LKTuDj0aFgnBccLDUN84/zxaqhAOCRvoFwN3U/REDACTED/Aw53XE/QJARe72d+qiIp7/gDT+Zx8KQ9txGiRn/REDACTED/Z6sqv+dCHbr31Nu8SvP/R/ZuZvZ5N1te83bXkHk1cS2v/SaTe/Zm0nUKpT37quv0HrrR9U3WaE/qQuPDrrv9091e3k9m/24zjat14m1a3FvcvXSv1hS/cevtttxNfB9H09eCpB7uizfUT/R4g1wHqoLV58oorr1paWsRHVSZqsfLzz3/C+ec/8aabb/6jP/rT6z/REDACTED/vnp6//9GWXXU7vh+rrAQ+4/6/96i9fe931v/REDACTED//1Fz7zmc+98o//tFtHWNi1d2Z2PpFL+O7xZHNt7cSxr3rqk1/4wh8+evdd3ejKcrHl973veX/x53/yK7/REDACTED/7sz//REDACTED/jCU983BOf+Libbr7lz/7sL67/9Ge21tfnl5aVqT/REDACTED/kP3pkviSVy/REDACTED/REDACTED/REDACTED/SmmBNtnu4lSQ4NQ/ueCEpqdBEp80xDP0rzAGvZ9b/el4RbLGyHAC/REDACTED/d/3z/e57P4CYtd31wAc/otsB3nPamThhs79umvu90zhwbrod4Jc/+9nP9Cz06i/REDACTED/OQnvf51fx3pUuSHtzY3zz73gWpmds/Bezt9Dq8yurF0rFo90u8Af/q6j/c7wDkHMKQzV3/REDACTED/D///E+rqq/REDACTED//Kt/9j/+Yve+gzP9YWnOfrspnt0B/qd/vKTKaoauX/21l73yj/9sObNLb/i2cfzw7d/yLc/5o5f/IRlLbVsbG+vnX/REDACTED/vGsZz2309jdB8/oD60SdVXr9eN3dTvAV1ze7QCfE/WtUDNwPtg719bWnvvN3/6Rj35s9/576WaG2uPqXf0O8Cc//uHl5WgHOK5HbMuiq6/REDACTED/REDACTED/REDACTED/REDACTED/i/REDACTED/SvaThlrTXkn+20j/REDACTED/REDACTED/REDACTED/REDACTED/u1Dk00dHBNaU7MRZ6CaY8/REDACTED/REDACTED/71uN3H5psrPv6QxOuTr/9BsiTHMfE0cEv/deX/sgP/+DK0UOT9XXPK8+3TnQrR+54/OMe84qX/z4dC7DRi225a35+4Z1v/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/qMMtTjGwJT+Dd23Ze/sPlA8jjpom/REDACTED/EQIvqVoh1SXc/REDACTED/REDACTED/REDACTED/M7v/miH/REDACTED/REDACTED//ZX/REDACTED/8BaxJuDR1PZlRWN6+5Kd/REDACTED/gWteXQb/zGr/7kS/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/kZHufKzZtbKsUo2MD/REDACTED/REDACTED/REDACTED/Cfz10VI/C+N966X/REDACTED/+J3W4mZl6qesD975c0Mf31e//vb7/wR1882Vqfn9+r+6lNv/G4e3n54ouGm9C6oNvsevkf/Pfv/REDACTED/NOf9tXjW2HXRRde8JrXvLZbXplb2mN/finSAX+1J452FX7Pd3/XaaedWmoUW/7xH//JTiHn9xwwzcrfD+nue+xjHn1O/wq00Le03twocLxwySVvedvb3jG/REDACTED//REDACTED/k3yxfM/cZXI/8V+m3n2xnV3P/3s/REDACTED/Z/REDACTED/REDACTED/REDACTED/6EQrWjtRxO6Vt2Oiq6kczWm9jmPm+71k0t5/Laj/REDACTED/REDACTED/G/CG47TVFjS++0ECnmodvh4N/Fc0A8XvvIWjNhX5rq/vEeZWaIhIG/REDACTED/REDACTED/e93/REDACTED/REDACTED/REDACTED/9EU/TDmWTjy2Njd7t9ENHocP0vUnf/REDACTED/REDACTED/97M//du/899n5xdnFndFZwQ4n9MZo+SLuL8i3tL7tzSwW39I/REDACTED/gFBQfu/r/REDACTED/REDACTED/REDACTED/0Og/xb//2wY9/4hPUYSkubJ1E1H//94/REDACTED/REDACTED/96K+cn58/cezwcnOq98nQ9ocGm1OgLxMculK3fuHWf/rnt49SrC/ceuvM3ML84tJW/1o4bE36Q6Gv//SnTRPC9co//REDACTED/70L/7lbW/3HPTXM77+6777u1+w4F7QFcZy6qkH7zx0eKv/REDACTED/+x9/8c53vRv67/rO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/vYBSSVJ/REDACTED/YxX3n/+90vYYfRcvPYzPxC9jeiiz6q/xkYrR/6kAdffPGFItNf/devfctb/hHGXLNzCwu79jRz8/2P1tgx8lcHN04chf4N1RcsL+/2fSsKvv/REDACTED/3m5/lKd+3a9W3P+5bf/I1fm50tTRp//Mde+Hu///REDACTED/zDm/2s6HZzfeADH3zVq179vve+0x4VLl4veP63/+Zv/e7p+x+6d/cZm1tr//7JS/bu2Z1r4k1veottQvPyf/ynf77zzjv/REDACTED/rXf/Rj/27/ubG+8cpX/unC/MJ/+YWfTSbY7nrxj//oL/3yr3bmM9utYkg/2ru2td7RF/7ID15w/vnRs/Si1vEVD33ob/3277ZbWzN7FiJddXj9BGzoxz/REDACTED/ww3N3FyjjKWsHOvqufD8J+yyr/Gzoetuwvy8b3uBr6HT4W/55uf82q/9cq/DOuaSH92LXvjDL3/FKztON/REDACTED/Xx7Qo5C3uN4RdL/OTtDhHEvN/REDACTED/5kYG7jc2/aD/REDACTED/Id/h/REDACTED/h4G/FYay55ZKrDYAcxcbi/Jr6HOsMYaINcKdayaoBIlV0Ks/8G/5k5/REDACTED/REDACTED/REDACTED/5lufrfNJ/REDACTED/REDACTED/o2d/XYb+83MrH39+/d+/REDACTED/5qEemz3afHj161GKXoZm/Dhw4sH//REDACTED/6y+JHtvX7P6BfsOgm3njeMK/Rp82u86yGToe7xamnP/0Zx48dj54DYlPdMlNHN1ZPOPfrfUub8UUxRj/REDACTED/T4/REDACTED/REDACTED/REDACTED/U1y3bEbQ36mwXTt3YCariSR0jrYJTil/yvM7/REDACTED/NcSbtDWZv1KnoIQsJT31xrcqg/REDACTED/REDACTED/REDACTED/fl/REDACTED/REDACTED/REDACTED/CW3UxKjPxOh/REDACTED/REDACTED/Iu3VVVe9/xGPeMSuXUvArr6/REDACTED/Ybm62k/5LyNded/3DHvmYP/REDACTED/5Cc/REDACTED/Av2ZrglRgrfednt3w1lnPW5xfp/WW5PNjbWNo7ff+akbbrzx797whjPvcx/REDACTED/xv3f2Le/b3O8am+Y31E5urKz/zc7/wYz/REDACTED/REDACTED/jd/REDACTED/OGCemtr4nR4dr6dTKwOX//pTz/m8Rf80cv/REDACTED/K1BIMPp8Fft/REDACTED/REDACTED/REDACTED/F/REDACTED/tvwFvuKDc6HJhhkNsEd/8m2AlchQeVY/REDACTED/REDACTED/REDACTED/auCWduwQbBli31V2HLMDtVj/yugrByI/REDACTED/REDACTED/eNIi/P3f/8OTnnTREx7/eDZSI7vv+a7v/P0/REDACTED/AjLX8771ub/3+y/REDACTED/+FDh7rblneddtr+B/apf9PNBlun1b2oW6do/dwKE4iebYZ7Jg1aXb27++cDH3D/REDACTED/ygB+VaednLflv3L+Qvdg1tGZ4//zued/FFMq+uu/76tdXVbm95fnHZ+6Wluflu3viud737b17zV/ZALJNTMQ/9VU99Sv9afueP5uYiTdja7I/U/sEf+N5uaJolTH0173znu26/4w6x84tLS2960yWdWswu7AJBb/REDACTED/X44U6H3/LWt77iD3+fxDHyrILnPuf/REDACTED/7P221rFv9/REDACTED/REDACTED/REDACTED/0/REDACTED/TmuiNR01/CNUTcMzkB3kCkyDYgKmL/REDACTED/REDACTED/93dvOHFiRWRw98dOlhZn99/39Asefs4zzjzwKPQpylPXQ+ynzRza/pTb/s23/sWufhvGvAXXb7j374Dad/REDACTED/REDACTED/0C3bN9fO0B/REDACTED/I9/REDACTED/REDACTED/REDACTED/bu3hsipqEYT5WiOIm/REDACTED/REDACTED/REDACTED/lsBIwGSK/REDACTED/REDACTED/UxNJub0/REDACTED/LOnh62qexus07lxctxVV73S+Xx/Yq8RjtU7my2K99yHIvLVb4c7PIpt/REDACTED/REDACTED/REDACTED/QuQ3fTwMlDH/KQK698f+o+V1fXjh47/rrX/REDACTED/860eFr4z6Fnt819Gj/REDACTED/oa7Preydhh9l93aA7Qjj3vB7d1zn9mZRhP/f2Lt7g5fe931733f5Wn90O/REDACTED/REDACTED//REDACTED/REDACTED/cMb32S/REDACTED/u7v/+Ho8eOvev/e/f8/REDACTED/+8DVN954k/8A+9O6bgBMzOv93hdNjMZ+/BMfv/a6WYnN8L5uCcDY+GR9w33PuH+N/6qFhUUWN80QtrYmNsBNNteJjeu5xaWNtdW/REDACTED/REDACTED/kLGHuNLdJ88rU1PxO11D9oAPr40/THw8VaerHiI1TP5/YgiIOVBErkDGqkZVairuppzkF+tH3v3/REDACTED/FQx8ivdPb3/REDACTED/C9rSbu67ttrV9iM/8gNPuvhirwj+6iYY3ac33XTz+ec/Yb7/ydlY6b7ykY/40Ic/0szPNc1M1HKzcndnQRdfdMGuXbtc0CK20P/kjJmUOhONAAAQAElEQVRJmB/1DVG9S+zWTxz/3Oc+/+Iff5E4oH7WofX6+rE9u+/REDACTED/REDACTED/3m55rvggrX61//d90Ne/REDACTED/iO3/rNX7dNRLlQ15E3v7k/O/peBx+8Z/m0rvjE6l3dZtHXfs3TQU7l4ft/4Ie7+2eXdjfKf7XG3KnbjRPHu/WOjgM+maOtnXfeub/0y7/REDACTED/REDACTED/4Qt/REDACTED/KgTQ/REDACTED/DfgBIHTKj9sSy8Q2EKADi/8MkCV3lI5ym5+Qu3cUjmRx6bJ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QahZl/Sl6DSO2/REDACTED/+R/nl9amlva0xebY7e1PXy7/yosbG70J/Q+9SlPCQGZXO95z3ssuOGGGx/4gPuHdnC03/REDACTED/+deex/Ufb5rbt/REDACTED/DXVXt7P64y/+6dtuv+v0ez2sa8U61LZtaU/8qJhudzPtwzcem7tjc2ttc/PEiROHuukNTk3DLITWc/XV13RodmbXpLUnnge3kl4//3P/REDACTED/REDACTED/rws75udaObl6o7jl0/aTd6bObDn/REDACTED/32vzodNtrpN3a6eruRv/REDACTED///REDACTED/REDACTED/YjeZFm4YvnTDS/REDACTED/zJ+ZZtFeQ0g1CA5NUG10fgRHBjz/REDACTED/REDACTED/IqX1A18ZwLS1ITbH1s/h+Xj5IdUJbx5RGu5MYXZ2ay9C3FY/REDACTED/REDACTED/CK2TDQKYbKzNzs19/oZuhnsDJD76da//u34sSr3mNX/ztV/REDACTED//Udde/REDACTED/u7f/REDACTED/9sR994cMf/jBzqnPouX/2jjsOdyJeXt6/REDACTED/nzv3jV6urqGac/REDACTED/6Sq1M0b7VZVu7VFVWhro3+/fWnXcvegvx/1R7/pzZfaifSrX/REDACTED/REDACTED/REDACTED/k/qlrH/DkOJiIgn1w8mI7I1jyny49fDOtxs/7xa/REDACTED/vGPs05gOYG/REDACTED/REDACTED/8gxNvt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xyV/REDACTED/fv4Tn9Bt9opDPvM+9+n2Kudn98zOLjSq/yGZAwf2506BHnvt339Kx/+Fhb3z8/1PMXXtr84d0/0r0PfPNXHeuee96Ef6l11nZ2dPv/fppx482FVSFta3ftsLujpPP/2Riwt7+qnUjDsF+slPutiv7k99dYL7nu/REDACTED/REDACTED/REDACTED//9jHO20XGfbVX/REDACTED/e+9+mn7Nu/b99efg94SwTzu1zf9d3fD/REDACTED/yM9zkDPkpFmMV0e5V9I09NzP9Nm/REDACTED/es+f4sWMrx4/zSZF7YRsjYBof40kUi60+x4tnD/R+Kaa3+EUhG/REDACTED/REDACTED/REDACTED/eaZMt/REDACTED/REDACTED/REDACTED/00re2k60ZNvnxlk/REDACTED/REDACTED/L//y9j177r0wvxunYekb49Nct9zyhf/9t3//hy//o25LfH5+171Pf7ju9q5srqD7vdn9+/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/gGjamuYhLbgwxvMWl8/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xe19x39pqXargYdsf/REDACTED/REDACTED/cXDuu55YAc4P5ud0zM/Nbk83LLr9isT/REDACTED/sdm7jx06D3vvQzGXC5CJ6M+fKQ/REDACTED/REDACTED/zhQPOpmpv8h3631EzPhV69NaDGnQH/REDACTED/REDACTED/axuU1/REDACTED/REDACTED/ZJ8rCZ/REDACTED/REDACTED/REDACTED/kYco3q0zu/REDACTED/2iUUM/MLXCK9ebZbGwcPHnjWM78epDr//C/+V/dIN4PaUmv9S86LC+IZxQ9/2Ff8xm/REDACTED/7f/fnJy8s7F5a3L++MQvmFOinPFk+P3nsdWD//REDACTED//2xf/REDACTED/Zaf/qn/9PXf8Oxbb//YAx/4NTPdjnr/CvGsVWnPqMju7rjjzl5vm7ndy/REDACTED//egnj68dbo/3B3R/3/d+d/Tusb3e8A/90dlz84szcwv23O+f/REDACTED/REDACTED/BLAc2JY53ynP/Ex+/duy/tQ/fQG97wRuh3zufV7Kz1MMw/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//7ZCp821ve0d/22Ri+/REDACTED/REDACTED/ut3/+DV/Q//gSwb9/Zc3PLbWt63mtD/61v2NHr/ve778c/ds0Lvuv73vYv7zjv3Avm5/duTfrm+uk9Xpa3ntrXmDtt7C5XZkXXd69/REDACTED/8yj8U73zet37z/REDACTED/S/hhfq/REDACTED/REDACTED/REDACTED/REDACTED/9ba1Inl+eC8SZla1Yp7pFNAz1Kpm/REDACTED/SqTpEjiB6ZVGHerwotV/1ETCdlmIu5/JoRZQka/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/r7N/REDACTED//qo8CazPUG368bKidu9/VpvPDEHRF911b/Nzc2JA/3sZz7Xb8xuHJ+0mxub/RdTDx06PPYV6Nx16PDhvvL1u/REDACTED/REDACTED/REDACTED/kG7r/u6VLxgdU6urh7qSJz3p4u4RUWcufcs/9bxduRuMdnX69i9ve+fycqoq6v4PuL/REDACTED/9kZe85Ge6fy4s752Zne9/REDACTED/REDACTED/ExF0/REDACTED/k/REDACTED/REDACTED/REDACTED/51pCRus/EwGCeafzPBZnI5nFDTBfC/dAQbDvjysNgkWm2fv+avEKqGbYv/REDACTED/UPcKHz9rD/xcqaxv1/REDACTED/REDACTED/+zhekO3uq/4btif/REDACTED/REDACTED//Dd/63eh7uo2Pz/8oY+dfvrDdu8+HdBW1zb6w2YftO1XoN/REDACTED/5mf/5v/4yLe8G/spX/MEznvH1uWnwb/z6r/zcz790a/1Exy7d/REDACTED/mxH/REDACTED/4Vf7L811n/REDACTED/+N36c++ckNHj4XXetrPUvNj4c1qZ8h/REDACTED/CvKDeZOCLFHc/REDACTED/REDACTED/H6j19XNC3xjBd8ql6bc0r5ajG/REDACTED/ID8S4AhJUYdK98/Ynouu8WUOXEcah0Itog8xzuPUPjfk/REDACTED/REDACTED/REDACTED/REDACTED/exPp+MSLzvJufvYzWec/vDe/vqJQ/17w25B2Kx+d4nfZGtr/ZRT9uVmv911+x393rs5PKnVMNDOddde3+1OQ/V1yr5zlxb7t3atVwHM2YoD6LbTt3I/2uSvBz/ogd/8zc95wxveeMr+s+bn9sQBb6qr2/r+9ud/94te+MO/89svE2/44R/6/l9/2W/edsenzjv3id0/jxw5kqtqYaE/xNscDK592AUTdrfatQ6cd9/zcs/aE6T7X8yyXxUAddfR/myqh33FV+R48vM/95+jkkjP/REDACTED/9/REDACTED/Q6PGN8o/REDACTED/REDACTED/REDACTED/gfkuuglB01f7/v/REDACTED/hm4f/Xm9XrbWqVk177/93vva9nU6d9dW/dtWqVWusql2lpyqStDK1o/REDACTED/REDACTED/REDACTED/CJv4VEY1ErIXI45CEkXvB83TgU6Bfte73/PEE0+qWa/wtC53tr+HUBj2QdrSKdAf/REDACTED/wFV/gNsQGCoyuOH3uuXr1sccfv3HrkclkQlvjZq3tyNvf/o5ijG3jE2dutrafhjDKXVRuEXv+C57/REDACTED/sv/9V//7mf74DP+szP+Fvf9q3nzp2tVf6nvuorf/pn3vT0k+8/d+EhyiElejSjU6A3a008/REDACTED/88Pfc7nfvbVu+8qvvuyl7/sl3/REDACTED/zUu3dzU1Lou6d21tPdP903dk/3H7owQf/x2/8Bhzr8TqN0i969at+4v/6dwc7W+5aXWd/3CnQ73zXux555NFiDV/25V/VpdPJ5Ev/4Gv/6l/9y930BFY02Dd/0+v/9//jH+5v31pYXFHrcvZXckHf/uv/w+2SSLQLnwLd/dEJu9Yb6Dj/REDACTED/QxxVNn6/REDACTED/REDACTED/fr8yHvxC9F8W9N7Pcm/nA/LDzD3/SS7Mzht2s/REDACTED/REDACTED/spbIFWg2OQ6VxfzRLyxXkBp6m86oRX/KSF9OBwCZMCvDzoz/REDACTED/1fe+gFL4CTeF73uq/9u3/v73eisbZ6l/REDACTED/+qr/REDACTED/HGN/4MeSvvfe/v/oX/519597ve8cKHHoTK87qv+2v/6gf/REDACTED/efPyxRx/7mq/+08V33/ve9/3yL/3KZGFx0kxv3779yld8YW11vUP7gx/68NKivcLKuwHd/w+PLM//gVe/sobe733gg25Qzq6tXex4rJsH6f58/eu/7kQOte6eCxcu/MRP/FtoZ5PFFRbZvR0nhi974P77yu+4Eeli1P/63372Xe9+9+/+zrvzrf4ksx1B3vCGH3/REDACTED/iy1/1ylcUFd/REDACTED/7fHqerWQid6WWk/5GhpwaMOrC5dzG1e1gkh/REDACTED/OoNnNBN7v4u/PK/6Y74sZwIdGnBxSNADVID/REDACTED/gR8hjTG7ZoFb03hs3ghvwPdOjHaZaPKt//gBjKRrD8RTDoX+BEUj4B0f/REDACTED/IwZgiU1C2kqKHk56pQdB0w/Vixhe96RUMCYwKADcQa/REDACTED/9qSpGJ5OAK947RV49AqnmhlhFvBgvFqY/REDACTED/REDACTED/m8hSRfDT5NpibZ4uL/REDACTED/wjf+RLa+U/REDACTED/Fm26thjgJF12FbY69cdZDzTR8JG/r/qiL7FReuX59r/3v4Hduvwxrh+5FRjxkMUBVojdf/bSzjNn7+l++u3feW/trU97yYu7dG9/Z2l5A+wu6Ju1kq95zRe7kpuiw+0Z3d3/9/c2u/zP+ZzPrr34oQ9+uEuXF+3R1t365+3bT3R/REDACTED/tgf/5OYjSPPWDXN93/REDACTED/8B808RZJ/REDACTED/geWlTJKqjSG6GpdMHu1R/REDACTED/REDACTED/zZOPQOHdwSGXLbU6KfiJRKKoHz4pE/REDACTED/REDACTED/REDACTED/vLq6ArNDfUqzg1m4M/REDACTED/REDACTED/REDACTED//uvvCKdAq/L+FOjd/WeNKNFOJre2nlrfWH/i8SeeePzJYls/9/O/aOyy9mRv/ybKWdZ8CnSp/REDACTED/7kU091Bc5ffH7TLNy8+cju7vZf/Et/9Zu/6RtrtPqTf/LL3/REDACTED/4gQ/V3n3qmaeNPdf6RmMWOuDN/+k/REDACTED/9N/+a/Gncqzs9uVhM3tJyfT6Sc/+QjvTz4JHvuMz/j097//REDACTED/ie77v5S9/REDACTED/REDACTED//C7/REDACTED/3funPXlE/REDACTED/qQ8Cu+rUEpBJcPKwwFQPk/uF4XU4Tbe1/REDACTED/REDACTED/REDACTED/qyl37uC57/REDACTED/uq+7w2ONk+eLv/jVv/REDACTED/PdPVtnf+zHf6J7cW3t0tLSBtCnCr2nQF+/dr0rMJkuL9ry/Q8Wc/REDACTED/ns3/emN715a/Opu0/REDACTED//c2rvPPHMN3bO6drabX1haXKyV/MzP+PTv+q5/vL93e/H8C4VtrLO9u3Pr7rvv+uN/7I9A5fmO7/hOh//lhenqwcFmOzv68i//sld/0cnsf6bn9d/wda/7hm/q2GNhyc2nuOm8l7/spbUt0KQ53W6Ixcniytb1x//F9/zLTzz8odr27zf80L/6Y1/REDACTED/fvNFFJ9/73f/0VYpbkhd//N/REDACTED/REDACTED/REDACTED/4lhICN/0o8pxOObpVFtoJgy4rSI/REDACTED/qFKF6rkrZqpwQ7OS/klhd+wuHThq/2nsVKQ7183BhuDkXRhKh/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/25r/kzXbqz86xz3MBU4sn46by+w25x8vatRz/1qXdubT7xuq//2q/8yi+vle7Wjd/REDACTED/L2/Xyu5sbH+ja9/3d7e7d2dm/REDACTED/Ov53//REDACTED/Za/REDACTED/REDACTED/2KyB9zYvepVr3jg/vv3t2/TtikSOYkyjfxbepc6dXh4tLe9d/Nat9z89V/319yN2d56Ry/REDACTED/hUh2OhR8hRI/REDACTED/tR8PGc2NqiWBp3Y3WrYZACubBNCUt3GG/Kg8eR16GZ2VIe/REDACTED/REDACTED/BitKc8/REDACTED/REDACTED//ox97+Ju/REDACTED/4iv/m3/jm1/zmi+m46+Lff/t3/ndw6OjjY0rO3s3jPv2bna4C+EU6MJbH/REDACTED//xTW9581v+cxdSFrF69atf9X0/REDACTED/djDD4OL5Y6O9qcLy12xX/ylX16wN9AW+vL617/u9X/REDACTED/spvLJ0ZnunW2yH25uPu+ZMsXy3avoVX/XVUNGS3fMjb/jBy5cu5610vV5cXDzc3zs62LPugpwC/eijj5a5xQnn7OCAMrrl1gNjvvGbv/Xc+XPOYyn0/Wu/7q/+b3/REDACTED/ot3/Sa17z6rW//REDACTED/B2ibz82EoLoj4sI8n/REDACTED/Y4HDWGCLzr9h3VSKe/REDACTED/V1JCkYMT4/REDACTED/REDACTED/+A0/REDACTED/t/4jXcCYs2na2ezBx64/77n3Zv/1L20urKyt7fp7tF1U9hDp0B3wNWrd//B137JK1/xhV3J2p5h/3zHd3xX99a5s/REDACTED/QKdC1LdD2FOjl5VP2lCnrPuKFiy/41KO/8wu/8Ev/8nv/ea2Vb/rGb/jef/n9Lc5WVs/a0UTsVobrp0C/qStw49rD+U/dW2/6j2/8vJe/rNbQ7o7l2KXFjZXl0+vrV27e+MTi4tKrKuv/X/QquHnz5t/9e3//6ac/QDldGPzWX/REDACTED/dL/857fxdKzOWzDvYPanTullX/w394493nP7MTyY9/REDACTED/84R/REDACTED/REDACTED/To/REDACTED/REDACTED/OFApTGeNhRoq9OmAg/REDACTED/REDACTED/v7BKxRQ1EYIHQgpc5Y/REDACTED/REDACTED/3fO+974bsQ8N5zFEz1/6y3/tN9757uWNc81kggNdgH/1/d/7T/7Rd8I8z0++8af/wXf8n8+7+2Vn1+597Mn3dDlf+RXVbcY/+ZM/BXYVdCn/qVt27FYd3/a2t9/3Z/9M/mvXrz/1VV/REDACTED/9CMfeh/M83zkYx/7E1/+1WtrFy5cfH7352w2G/OWFRM6jBVwcenU4tL6j/34T/zD//f/cfr0qWL5v/23/REDACTED/C/8EUvfMHzH/jCL/j8L/3S1/bT8A0/+uNdurp2roV2bf1cFwB//w/84KvqG+C/6a9/w5d8yRf/s3/+PZ967FOf//mf1y1pdgFtrXC3Cvpv/93/PZ12i9Cnut7v7d3oMv/cn/2aWvlf/MVf7tJJMzVN+iVqR8DZ0cEbf+pn/lyJu7rnq//REDACTED/6Vv+5vt/9z25DNLz/d//PX/REDACTED/t/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/3tW/s7sbDg1Wz9HR4Yc+/JGFhZV77nkpeGsvduzwYOfxJ37nX//wj9x7773Fhl704hd1ld/REDACTED/vNnkWXUpHNPMp0Cf07O/REDACTED/8l+sNdTNF/z0z7xpe+vJbrrBJKdAx88f+AOv7v4r/mSP8q4/BwcHP/uzPzddXJ61h0S3lZVT//W//uxP/fSbLl262PPiX/qLf4GA9/5u3/TBz/73n+ti4LNn79vbu9Xxyc1bj3cdue/+59U68iM/+uNdgbvv/n2TyZLwVWOQteKjj73zl3/REDACTED//1D3/6p31arUd33333E088sTBdhoYNZbwFuvBg/REDACTED/gay/REDACTED/REDACTED/REDACTED/REDACTED/Xkvf6m9S6Y25OPiXv+85S3/REDACTED//j/0pa8tlnz/REDACTED/vt3/qdV77iC4qrjp/zOZ/9d//u/36wv7l04UXO4uMrKqdAz/v843/yzz75yCPnz79gdfV8YCsDh/REDACTED//mf/45u//vu+xV4WVns/93M/+qZ/+j3t7Nx988Pc/8fjv9ZwCfeznv/23/24HdP3K8vIpotu5Cw996tF3//i/+Yn/9Oafhjt7Dg4Ov/KrvrppFs6de777gAEO9i3//MW/8OeLXe7Kf/REDACTED/yhh97529Wp0t+7Ed/6Ev/0B87OtpfWt0wbumpto2/REDACTED/XDPvFD22xnvzP9PQ/REDACTED/o6FPo+bslTF/REDACTED/REDACTED/iTEJHVf6Dm8wR/REDACTED/Vf5aDm3A8eSNHYLpG3amISWUmHAvXqD+SA/REDACTED/REDACTED/4S/82VqZX/REDACTED/8l//2D7/REDACTED/T/wg7VXurDqW7/lr2/REDACTED/8lV/5tXe+691wZ88/+I7v7FbLL116sf3DtLO2+2vrxS96YS3g/REDACTED/5zdXL2185RbKxn1iFDZ/02ayeLK2gc/9GH7KXLl+YLP/7wHH3xwf/REDACTED/REDACTED/REDACTED/ELMawJ07/REDACTED/REDACTED/dzJar4/REDACTED/REDACTED/TWiZ8wbAQepJ8z/sbeccRrxIc80KxrTG+3dV67u7u3cuHkr/REDACTED/5R/QM9TthH/REDACTED/REDACTED/6d//3T9648WjrqCanQB/z6XjpJ/6vf/8ffvKnoJmcPvu87Z0b/geS96PDPQinQJ/Ms7e/D/REDACTED/XG41y3RxYWHpu/7R//m5n/s5CwvT4ruveMUXfvf3fN9HP/pOsFvHN0+wF4eHR1//ur9+89bti1detLd/G5Ru3DhzZXf3xh/6I3/iR374B8+dOwvHet761rd/7/REDACTED/uSswmS5s71x3ZKKvQZrgKTgf+V+/REDACTED/ydd/9z/9JrWtf97X/y9/6X//O/vYtWvc4OR5ultY2Zgf7Y/REDACTED/8t8etQ0Vz7scof0/GI9ydnqR/eZn4yzunfFvJz/REDACTED/REDACTED/V9UWbRR9Gi+0bl8O10dwkxrINCBUwXBGw/ngpplhM50uVJRsgScj/REDACTED/z6aG565I7BfrlL3/pQ/REDACTED/REDACTED/7vuMffHuxrdOnT/+7f/8ful40jsPn2j6aPJ/45COv/REDACTED/REDACTED/7a/+lVpz3/Y3vvmf/rN/0QGnNjZOqhfPPHPtT/REDACTED//mt/2v7/3td62trcKcT7d6/I/+8T9tmsndVz/Lz3ZtbT7dNfC6131t7cjob//2f9AVOHv66mS67E2es18UPVm6PfnU+37rPb/9qle+wpRk//d/3uf9jb/5/REDACTED/REDACTED/REDACTED/Ed1/vOAuy+uPJNEw3fuq3gYkyBf+UjeP/REDACTED/REDACTED/2BJGI5bw/g2bmZFEgT6h/4EyWQYNAz+lSEYErjNYUlbldOqNOQk/REDACTED/REDACTED/REDACTED/REDACTED/wT8ZOFBDrdJKtnRDijxHD0v/c/UctYcHB9uv+MIvKEa/3fPxT3yyS1dXzrVI/7My6f6dsQ5o24XJahf2/NIv/Qqrs+zpQnewMeT1Y9Oqa+W3f+e9r/2Df/QzP+ulFDmcv/CCtbVzgfOw3Ti9dvXqpbuuXr7/REDACTED/x9779H9g7YyvPt/3Nbx1/FPbg8+STT3XNPf/Bl7znt3779OnLL3/REDACTED//fQzD73o03/9Hb8xvv5u3L/7X/REDACTED/REDACTED/REDACTED/REDACTED/W882taet8yWK9pdgb6/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/n0t+mZZexJG6zs1FDDE/N/xGtFGXyu801gbFKfPrXrC83b3/4OuwUa41n8fGZ0XP6HP/rRrs4WZ+bowG6pb5ouVLhw6cJJ1f/e33lfV+ehOzD50uVLb33b24vl/+t/REDACTED/6mfefOXyxWI9a+trO9s7zdJaV9uv/urbNjbW63jikXv2uiZv3nzf+97/trf9+vvf/REDACTED/yyKO/REDACTED/REDACTED/54i9+da3dFz700Ic+/REDACTED//RP/Ga1/yBP/9n/+ylSxd62u2Cuo997OP//Lu/55FHH+vqP3X6qpk0e3u3SRPSh89nz55926+/o4j/px63B0SvLG3s7d90lGE5b/zqjfvMcXFxtRv3N/zIj33Ja19TrOfuq3f/REDACTED/vHtzy6mxhcemXf/REDACTED/QsyGmS4VgGgolIpk5cX49/REDACTED/REDACTED/fc+PWo08/88FamU4K7rnn5csrdn3MmVqMhEngLkS/8exjzz77cK2ebon40uWXLC1tXL/REDACTED/f3duDknrvueuihhz5/YbpCgd/TTz/8vvf/Uq3wwsLyZ33ma8+euws8r7AtYB/g4Y+/56MfeWd/i/dcfdGzN57Y2bkNJ/Fcuvi8T/REDACTED/+pm/8zM/8jCtXLp85fXp5ZWV7a+va9etPPfnUz/38L3ZB6f4+H9bVrR6fO//REDACTED/+qmNqzduPPzM9Y/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ztraabcbz9DNumzwaD5MPhTr8vd2uh498t7f/REDACTED/REDACTED/33+/u7xde7br7kJa9o28MuvHz/REDACTED/REDACTED/boiSffu71dngO6+67ft7iwtry8cXCw/dQzH6J91/REDACTED/REDACTED/47wn7E2iVCqJ6PCuOeBB+5/4vEn9/REDACTED/n0oYkc/V5G1p+kg6bWezoY0oPtVxuQod8/wIHpECr8lDtFbPmyUA4ou8dQQ/REDACTED/REDACTED/REDACTED/REDACTED/Dw1rNC0vru/a4YB7rNjrmcsY84Da7dlldBGJP/c2emT2eF7pAyJ7TC/REDACTED/REDACTED/REDACTED/REDACTED/px03NhPLo50nNpuN0SfV/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/fl/REDACTED/REDACTED/REDACTED/lx/REDACTED/REDACTED/REDACTED/REDACTED/os1sb/REDACTED/xF4xGRB1eoksM9FZwmMQ1ebqbHy/REDACTED/fpWV8/REDACTED/REDACTED/jIPdCrDoTBckuztCjYubu9/s1ZsTM7m999TNrUcjGazJaSF/jB6o6BAP1/REDACTED/kjnweZZdLcL2PY2H/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/pj4b6i2FhsVfJrg72k/REDACTED/REDACTED/REDACTED/REDACTED/z6A7NupdfGkt3cp/REDACTED/Do8YW1jZX1t/REDACTED/REDACTED/dWBmebVYK2s/REDACTED/REDACTED/REDACTED/REDACTED/Ob0v2MzGdy9GYo9lRtzy4i/aMaBtvUYccAzU23LWh1dQ12wi3K/4JJ81R2DmxKyo2bJ52L9rLmAz/REDACTED/REDACTED/GZz7+mbm4/REDACTED/REDACTED/REDACTED/IQhQOWPUfqi0OnVoLBKwbYJTN/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/2/REDACTED/REDACTED/REDACTED/O5GmNPgb5owgQuniAcyX4MG7WSmQ/AQDrEylQI/U6uotMM/U6n6aOiM42I2Yy+s4xhFj/yK/L8ZEvACBFN0UxWBnBkmglQkdLlJ/REDACTED/SrlVjhlbg88kOD/eUicYlQdmY6nDP/REDACTED/iqiHgV+Tfrn/REDACTED/REDACTED/tdMLy6cW5pbWlitxU3t29uP/qJp248u4n2puiZ/REDACTED/REDACTED/oyJm1ZrfGI1LNka6p/1jPoJWI31pr/REDACTED/REDACTED/lTzqwaDD1L504UN15+W/REDACTED/REDACTED/0G10UEHc+7fc7d/REDACTED/REDACTED/REDACTED/REDACTED/ZMK1cvrs/REDACTED/REDACTED/REDACTED/pkpTVV1Ie+oMaYF8iijilNgBaHobS/REDACTED/REDACTED/REDACTED/BDYLZrJoYMGGwTi1Ya/d/REDACTED/REDACTED/jO6sbRVho/REDACTED/REDACTED/REDACTED/REDACTED/AcNC3QNmcIdn2S/REDACTED/REDACTED/REDACTED/vGm/REDACTED/VXY0KHCGJ83EcPGn0bhU/REDACTED/REDACTED/2PVwsd0/sAxthjrqwQ0Ne/REDACTED/REDACTED/RjPfHG0bOjS/lu7VWOa/REDACTED/c/sjewa0C/REDACTED/esO+XL66qK8dkrnWug/ZlyaHdldVrMIhJ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Ku8kfrk3h1RdO5FlzFvBQ/o/REDACTED/REDACTED/sQl/3ua/REDACTED/REDACTED/REDACTED/REDACTED/9M2IynekY2Tve+hJx2Ist6qc7/Y/REDACTED/REDACTED/REDACTED/d1Zc/REDACTED/q4xO1i2WEQ/kEbzlUDFTfIV8/REDACTED/REDACTED/Xg027m5/REDACTED/Q3YxlPgex/REDACTED/REDACTED/REDACTED/REDACTED/6xyeVLl++6comc/REDACTED/UGBr3F78ruB0ugft010YvLC40kwXD/REDACTED/Pr8sAVVd/REDACTED/REDACTED/REDACTED/REDACTED/4XbuvW/REDACTED/K3vsGQ+B9l5hW9khLy61/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/j6YdIEE+/2fQH/BJ/REDACTED/0Z/REDACTED/y/REDACTED/REDACTED/Cdrs9umXsV760LtpGbEG0JJXh/REDACTED//REDACTED/REDACTED//zfG5AzJ5ri3c0OEfKZvARWc3E2IOrJ0/d+sj+4a0+p60Mj9RLlXweloreq+rMQdyOq8/7bUSMm/A/GkiDkBwG8WHKdg1G28eaPRU/IRIPkaaKNS+ZAda9/Vuym2i7RV+qZN/REDACTED/mfmrwY/tsB73EONQoWaNVg/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/uJuO3QqwcWGw6daBm0ljJs9uP/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/YRxy2DGzSRYpfyZcenl0w/dd/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Xi8G4JlYw6w/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Ko4BMd+1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0YvRY/h/wNGTGeSX5ny/LfbRmAZqfPuYb+Lczt/5/Bwsru7c/P2s/REDACTED/REDACTED/dhId5OJZzbuuXrv+3/REDACTED/REDACTED/REDACTED/REDACTED/gGrclBq/REDACTED/Qvgd4T7if7QVbl8CNS4Q+zECGliodC/+X9RDagt1AqQCoS/IRaUmeV+S8kin/REDACTED/O/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/MVr4C57XPuXV+eYF8nHz9j/REDACTED/xQD/GSuxCo9LKCVbt8FgM/REDACTED/9OZk0ze29p29tPTZK4+Gd6a47cNz/REDACTED/LDyoIWXTUanJYPLH+wwez/Te4GLK71aD6sz/REDACTED/REDACTED/REDACTED/REDACTED/+fkggJUzdt09hzcun391uazpP/REDACTED/Yln/REDACTED/LBZ+Zfae/REDACTED/REDACTED/REDACTED/bD2Sj1eWMS3lBr/REDACTED/6lS9ONLvq1i0o2+u2Yb8bf/fKNR/StL4s799wCrfS2laH3/XfLV0F6QtTcMlYtcvDEhtJzyfmzF59/3/REDACTED/H/REDACTED/Vq0Fowii/owaSYpIQLsScdiFga/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/M4z+XfO+wjgomgUdu1fawKC/REDACTED/REDACTED/REDACTED/REDACTED/6MYsDC4Hs3i/REDACTED/AMRATIhAD2YdI/REDACTED/REDACTED/REDACTED/niOsgrfDxzCkm1i9qCQIRuJeg/REDACTED/NtMMH2G+C+5vMOHD/REDACTED/REDACTED/REDACTED/pUHaTRFL/vHXNV0iB7DSBXTo/REDACTED/vYw2OTvhdSEyBABApT5ONtGymfuJ/REDACTED/d8X5MK085nOvNU/REDACTED/REDACTED/dtJKIuK065wNKm9FcMvHXf7NW9e3tm/REDACTED/YEV3/REDACTED/REDACTED/Ckie/REDACTED/REDACTED//REDACTED/f29nb+vw0ElNS7uWg/REDACTED/4FasiXIa3qF+i/Ij/YmZvsXY9MlhP8nYmefELsR2J7GV/REDACTED/ZH+yVX6mTBaI/REDACTED/REDACTED/DJy8/REDACTED/REDACTED/ieb9gD5Ywc6X6B1MPJeZiBWcv9aJWG/REDACTED/REDACTED/d3b9x4wsvnxK3L2gPtkE//REDACTED/WtlIXqlVqjsmJBXzaUluiiwQ3//REDACTED/REDACTED/REDACTED/2OhTQw5oKM4/REDACTED/nC29xnBG8S3Z5YzgSPCUlY/jRKylxpg0mVIdSCtWU/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/iNPLHFP6GTZbSouTXoZ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/m/yet/REDACTED/REDACTED/FZteyZ0A9282Nlx4eWrVlZZJZ/REDACTED/REDACTED/a++Qg+X3+PLdV3rw+wDJ98lKBS6m0ltCnlmpJmC+/1KxJ9XBEnxONNwtj5FN/REDACTED/CMaOx/Kj7VhteXzt17/qVt2/REDACTED/REDACTED/REDACTED/c22yXfBf7Kl1/2W7Mah77shcbOy1/REDACTED/REDACTED/REDACTED/SE6v6Py2WZSGqn1FJBv/REDACTED/r3965tbt7C9wn/REDACTED/jkzXrhDzbO58MccNpu9YcqVqDVTc3fq/REDACTED/REDACTED/REDACTED/GDahN/REDACTED/REDACTED/REDACTED/NBM/NNWn/REDACTED/+8JjD2/ubtkLvxvDXwV3MXDTTB+9/REDACTED/2DqGQPzzmD+w9yFTvKJxC/vgGQV7LgvM1QeKv5V5G/kqqGQj0FN5gtaI3wkrib1tQR9g/0NpzibTMnG/REDACTED/REDACTED/REDACTED/V2oqtrgKF2YTT6/REDACTED/REDACTED/REDACTED/ECmVUtbvYqY1wZQsMqpme+1LJV/REDACTED/REDACTED//NaGc9po1Y4n6N0DIEioqM/Dmr+FkO/REDACTED/ET9SF/REDACTED/REDACTED/REDACTED/REDACTED/GfRGsyKxqjgWJg0z/REDACTED/abjdmh81emIClA4RKRg1GdF/6nKr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/kC7GDZf9ove/REDACTED/9/REDACTED/REDACTED/REDACTED/REDACTED//aW3/REDACTED/REDACTED/REDACTED/OCC9eRr/REDACTED/REDACTED/REDACTED/bZJW8kO/REDACTED/REDACTED/tNUUlfNhh5QuNZAbC9Z8tGk/REDACTED/REDACTED/o2hXp/ok+hk6VQYmNwRTMvU4ZPFRw1dhE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/rS+XvPf86Mrzvq/ke7ndHt/REDACTED/WhsD21m7I7DrwEIc+9GvO/REDACTED/cB0pysZcyG/IObFi0ZAboZSLCOiGeW7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/srqSaoj21fqZ7EhFpePtx4/mE0sYearUNs2sw2+UJPrfxkm/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nFN4G4IVbC5JvLGu/DdyeHTxqZtb/dnfzAn3x24juor+62if2pl/REDACTED/REDACTED/REDACTED/REDACTED/O9OcIvSfBbaQ/y+UDZ8JYvT2g/REDACTED/iVV/REDACTED/REDACTED/FPTadF+apJjU9e/REDACTED/REDACTED/6z15xZD/REDACTED/REDACTED/REDACTED/REDACTED/alhV+w4N+J+l/OHQKzSgXVjtRed+tdQecnK/REDACTED/REDACTED/REDACTED/REDACTED/zNrVCSxsbj/REDACTED/REDACTED/REDACTED/5f1rzQ/iqHHLnmvjPLsZ26dHe/REDACTED/igmoC/jn9vZ8fAxnh58ap0xNX+A0hbQ/REDACTED/REDACTED/REDACTED/IF+kQ/REDACTED/gN3JU6Fhyuda2Oag0Anh0yO/RcLhEEH7UL586sEza89r7alXrVt/PXJOMYXBsu3Zlp85duKb98CI8ub9te5uW9p8S2bYl/HbNXlF0zrjLd8jgxfPXzp//pI1+y0jRWdUcdBr4Ya/REDACTED/REDACTED/StMBITjWdGbjxgg3cLB/REDACTED/l7z/REDACTED/REDACTED//REDACTED/pICxQTwvHvFuyKeN9/mgkHVxsSy/REDACTED/U7w2mZbWkVX/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/8Ag2hVKZsVxb/REDACTED/REDACTED/REDACTED/PGy6bUNcPu/KbvcNFKzlaKKw+xfjnS8hMG6/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/YXUT4j+AyW+BBXLuPwAU8ff6H/U8xDYPl+KBz8n/ALONF4/REDACTED/REDACTED/Pbxkrfh/GJ+ykI/REDACTED/REDACTED/uhL/9N/fwh6nu/58ZUrdIqXgG5tb85vPfF///lb9s/REDACTED/aFjW164eLGj/REDACTED/dse/I/gF/8C/9+OULOzcbPcOsJDQR6e7aE+/47hsOL0mxp1/REDACTED/ku2/ePz/Qlm59z787N9zXtLQZkoCdna3v/eLzX/HA/uanH/jl5fc/f6rpvt3Rzrd//rmveajN/Oe/tvzuZ24aDIZb2+v/4L9ffeD2hS5tX17e/o4fm9m3cKBp7+rquV/9a3NVlIuWbp947vK/fNeVS/XtszPzFP1w2t3d/Zp7X/lzb5Ve+9v/8dKnLtyo54GHmWGEJXrxJ//C4ebXT7+4+f0/Pzc3twRxbbfY7obP91Uv//REDACTED/REDACTED/REDACTED/YVXVp5yTDFZH+a6dFx5So3xVM9Eryj/4tUU+tw/eYU0BdL/jbFKfUiDxf8xX8j7SF0/yk++9jailzOmcmD7gsy+5bvlyI/REDACTED/REDACTED/REDACTED/TJxJMJ0A0g70mFCphqt5MqWTfjNMTzqUHfkT+nt/REDACTED/REDACTED/5Nl/6piPz/+Ev3/T1/9fz+w7dwpcthaYN/BcWZvHuGxb/REDACTED/REDACTED/0rW0rmf+75Tb//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Exb0bXT6nU7u096ARWU/REDACTED/REDACTED/REDACTED/FrNYZ/p8WUHDcC0/REDACTED/REDACTED/REDACTED/REDACTED/+/KZbeaPt33BLdAejUu/8vvPc86nXjo8197KB5uba9/wwNZ7H3+lgV+5tPHbHzvzNV9wy+LcsCl//8mVx16g4cxco0B2djfe/8m1F8+3E56/9IHn5meHb7j72NH9s80/X3MD/NTvfWZp8XAfD2i/oIZW7YFjz26+/OgnNpavbM/NDhZm29D6hVcuXQkz8cZdzdTra0+c//REDACTED/weZvv/REDACTED/REDACTED/vU2RMn2u/REDACTED/6iab3cTSin/ztp++8Yf/nv/r47Ewba33+bZvv/REDACTED/REDACTED/Q2fSS3S/4A5TC49PCy3nq/REDACTED/qqpE7XHJVplfhEp/REDACTED/REDACTED/REDACTED/REDACTED/SwlyUdxcedcuTyv7WwgBUMq/REDACTED/REDACTED/QiinIEQJNg4W4/+1a/+Mr/1A9/5xiZdWdt+2997F+d82Zf+6cXF/U3J5eWX/sJXnuQ1und8x8+fu7z5wrm1//K/fXnzz9fdduxP/7t6/74jjZLb3F57412XX3V6X5P/V//VB554cWXf/MyLP/VN/REDACTED/8m7Vtd3/REDACTED/+wVMX/u63PPDgnUdakuCBf/REDACTED/4rWtp/pHm5GRG4/5ZDR/a3U74/+r7NhYUjtx3Dt76uXf/82BPnT5969dLS0Qa3Jr598PbhQ3e3y5X//k/9we8/cd766NjRm9/whts4CJwZzjx8X7sEen1r921/vyX+X/yqV//REDACTED/REDACTED/REDACTED/uMTvR32f8bGuVDnsgmQljF/zDnj3CKMfnj7l1HY/REDACTED/vx2vaNJh4aRHMn+e/fyC/REDACTED/REDACTED/VmyHsTw/REDACTED/REDACTED/VcfZYez1TXIcHx2V7rLIqseQ/REDACTED/REDACTED/REDACTED/ZeahnhZhElFUVIYZZ1P/yLddKiXHILhlros2/fkde/REDACTED/y8V3/oiQ/REDACTED/REDACTED/cIuI2m9/REDACTED/Pnv2Cg6OijVrJkXr3be+ZpZ/+gc//REDACTED/yszBrO0pJlweDqpnDXMcMVaJNaUa/REDACTED/REDACTED/2S3GDTIWXf+CPHTx44PLllTH2wrXYPcVC2Q/REDACTED/E5ZaRNfFHV4yEoRZ12gtS3N3ZOao8/REDACTED/REDACTED/REDACTED/REDACTED/JTyUpmgINmIsrKiHlrXl7adygs7YZHH2/X/REDACTED/REDACTED/REDACTED/REDACTED/+pdz+/REDACTED//bO9keeWVnfaj6If+1rbvFS9aO/REDACTED/69rNR2ceuvskd8cP/REDACTED/REDACTED/REDACTED/EXgeU5a7gKsIgwx080ag6o/REDACTED/H52rga7G/V2P3c/+BxvobDq57fdd+n8dJVNZLlob//REDACTED/REDACTED/REDACTED/1Bhad/REDACTED/XccWbplt95pndB6N6R8DlW49Ijv/g0+vu6TIeD/ZN4WeCkkiI9AIGUQNGAGMZA6XUz1/PziLTfd1rRP7kJhOQ3yr5O/REDACTED/REDACTED/REDACTED/haN5SvbP/wdc2+9/+i3/NN3/+zffGuTs7Y1+nePDfbvP5x/REDACTED/SxmMv1n/q4aOH98/sjup1uHzj4dOM//b2xoO3z/REDACTED/R3fuLDT5xbuO/REDACTED/REDACTED/IObVQm/k8NQt8CIysoHQ8YIM3DAM4xe/REDACTED/REDACTED/REDACTED/REDACTED/cp/REDACTED/0QAwDMuBC0d2WnWaDnhVVZkbt/REDACTED/REDACTED/iVd3aN9sE/2+5+Nn3/2JS1x4Y6vx4IdRmCjRol7ghI4VnG/REDACTED/REDACTED/fe7kDW/Wrm2vrXrLPayV4YYji9/2hZdneESmgjuObZ/REDACTED/+03CXu1yniRt/REDACTED/REDACTED/p5mntwltqHYHn5cvOfEQayn/M0tTWRCXpg6kY/REDACTED/QnSiR/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/C/tsxLJBwneZrXdxQwMbXf/QT7ZFO61ujy5dxe2cjdJ3EIy8un3/0E+3ig0tXdi5cXJ9fWFq/svzhp2a4opfPX9mpZ5pv7u5sfeip1Vcut2HeP//Pn/REDACTED/20uywXXt89uLyOp7h/Bb1CteuLP/mR9twEdojrOFP/bP3vPrO+x8Nxzg/REDACTED/46aG09MKVI/REDACTED/8L5nd0b3XFp+ifHf2d1ql0Bvt8MH/REDACTED/8/7/nrb7//C+9t52//xz/5uh/+rY1Ly9Lena2tA69ef/REDACTED/Ulx/REDACTED/zqlyHAhi/REDACTED/out1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/UsH1QFqKz+zdeXN957gNbo//Qcbw/nj990Ab7m/Xep8/vLmyRNHDhw42pTc2rry0F1z/hToBpibW7zj9gdvv/11lV4YU0gRnbPg5DDA2zub999Kj9zXhpo//QFagRu5zSyNC3P77rzx8p03tAuD//aPfejo8Vf9iYdOPXLfweafv/REDACTED/76ampUvS0uNH9u0/xnQbjXbOrpzlw5ZPHd1/REDACTED/LaZuQVeoDMzHNop0Jvbu//REDACTED/X86n/8w/REDACTED/UhuB/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0u0VfCxHeKt21zlI+B66lI/REDACTED/REDACTED/ooL5tJVwKBRdV8nvDS0tHf/MhLf+zzTjXwD37j4D996Nk/94jsa/2x33p6cfEhfst/REDACTED/ef8s+/uw3vnH23Mpnm/74uY8szS8db42erjAAABAASURBVLCbnVv4yd/5w7/3La9tfv32P/REDACTED//REDACTED/hevnz2Pc+cDKdte7LBw2/+xpfOPPUP/8NH/9l3vqn55/d/5YHv/PGN9nRioLuObw6qNip+3x+98pX/629w+Wfe8Q3HDs7feHhmQOuIB9h/sTGRU8cWvunBc2GXqfgAv/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/U9rSB1xL/REDACTED/REDACTED/swRcXw5dPzK595vyRhsHuu/Pyo49vNDnv+M0nl5YOcm/+q1/REDACTED/nCjpXDrq/WSQOEbtnGpd4k/REDACTED/REDACTED//REDACTED/1MMc4T/8NLXL5mVyo99UJT46Ek7WOj+TU2MTGUL/REDACTED/REDACTED/REDACTED/Q0+aZgBDjuBSa/09VGqEotlwI2dJ/REDACTED/GETRy9fOnbv9H/z0R/7z//blvOa2eV64sP7H/vZ/vfnmzz9+/REDACTED/REDACTED/JZ/VDG3AvPLN//REDACTED/s6Gmhf/jO3Pzi4ty5h++T867/71/REDACTED/REDACTED/jex5//3//sG5qSr7l5+zt+YrZhzG/7koVbj7UN/Ps/9/xbHv5TTS2j0eilS+/jw6jraun/REDACTED/REDACTED/DD69Q/REDACTED/REDACTED/REDACTED/REDACTED//xJm/fvoMPP/REDACTED/REDACTED/35R/8xd//aFDJ4xXjHu6Q3gJ90voHzq+Hj3x5O8/9dSHi0175OFvPnjwOJekevQ77/REDACTED/uYlJ5N22C5tOH733vT/dlOdXjx+79Q0PfhV3E+uQhiB/+PF3nT37TBf/BvmHHvqaueFsU25ne+N33vOTo9Hu/Py+N3/RN8zOLTRVPPq+n71ypV2T/OpXfdHJG+6YGc48+dRjzz7bXu/72vvecvrme/k7n/rU7z7z2Y9xsVtuuXdQzTQkXr74yvs/+M4i3d7w4B8/fuJWXjNyefns+z/4i8ViD7z+vztx4jZzFMF1U/REDACTED/ilSmGVKDBzcRAzrTFAz2/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/YfnyWdIyqE/REDACTED//akPvrJ84ZXlFrdjx2++/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/v7wk6fo8k1RPlqrwKCdQ/REDACTED/MihY9SeTcVnPichPR/REDACTED/REDACTED/REDACTED/XzDEATJ1K2vzc/REDACTED/REDACTED/REDACTED/r4RQeF3ZbJ1ChOAcuTtc5RwlU/cWDrcy2OUz64sP/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QV/REDACTED/REDACTED/REDACTED/REDACTED/7eExg/lBBCohit7fdihXMPmC5mvs9jEt3gO/7Z22PT9QEvNmukJ9jCymK/gemMWGDq7HVdzHb75hY2GcWzoWf/REDACTED/tfnZDHCcB45pMTbpNEXMf6iA4tk0/REDACTED/REDACTED/REDACTED/cPZxZaM98blc3s/REDACTED/REDACTED/REDACTED/b9zTK/REDACTED/lpT0/rm6ubWWnhHNIbexQTqCagKEHoa/7V/REDACTED/gDTlOU/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/FkM/REDACTED/I/5e2QZbf3hQhdXzNEgUKlS/REDACTED/REDACTED/REDACTED/UIchTBNwCVtSXPUEEIsWULO/REDACTED/REDACTED/REDACTED/REDACTED/HyQNe0X9SWe/czDY7Df6nNklJBP6c+cK4JOh1A1Jc9lRhc/REDACTED/REDACTED/REDACTED/REDACTED/vT0Tc/REDACTED/56Gl0/REDACTED/REDACTED/oVKP1jEU7/Npg/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/MBYPryoQOz/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/WLKRHMqyo+YTxargzfz/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/aPKRnCYn6c14h/REDACTED/Mw1c+sQeCEbopCTkNFoft9zZ/REDACTED//REDACTED/REDACTED/St7SHhXSQJLauPolVcHvYI9lv8nM/oUNuf6BYGp1inCMUKC/REDACTED/REDACTED/2RfJuKrrEXE6+pBUlB1BdUknlt/REDACTED/REDACTED/REDACTED/REDACTED/RP+11/+kcKo/REDACTED/REDACTED/REDACTED/REDACTED/4X37DgDH1gRRX+lFq8TLieMiZz5hld1T/REDACTED/REDACTED/REDACTED/zmv/REDACTED/REDACTED/REDACTED/k/REDACTED/REDACTED/REDACTED/e9or1Qje/JnCg9ZMWxZSa9dPUolPWxHiWpy/REDACTED/9cs0dUMS5l/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Grgz7BAnkhKn8Xb07B/REDACTED/REDACTED/oiB/REDACTED/kmshpEANeYfk//REDACTED/REDACTED/REDACTED/lBEtVEDzFL5QT4yf/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/3aJUamrMNsjM0RgVoWOdCX2V/mc3h5Z/REDACTED/REDACTED/lXnq3l0B/REDACTED/REDACTED/REDACTED/8NkuzNNmb2lqZHPsJrG5kbYOKto0/NUa+9LqYCPp9Vkj2VS40vPBFr19+A0/REDACTED/REDACTED/jU6CTynwa86dy1iu3Ft/REDACTED/REDACTED/5rQ1+eWK7lF5Q9va3/z/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/a1SqIKYwHtTuCqajfNDQazz1/46Pr2RSgqHQ8bQWEinD5lMS6y2l7SsR/dGz7d/HrMhtH+fLoGfCbku+/0OIUTgth0cK2DTzG/4/OXkSvDBb/REDACTED/REDACTED/REDACTED/oA2K/Yo2P/REDACTED/dMI/REDACTED/Y9llaNFZi+1z/ihTZ8Ayg/REDACTED/ekUcvcDC7dkKDZlo99j+25+/REDACTED/REDACTED/VK1XB9fEAQOo/REDACTED/REDACTED/84z/iboweicUp1/a1LtCoZhWk5p1dSmIJ5KO/E0Jq3u8uLivgTfW1/REDACTED/0Nzs/REDACTED/LVqmXWlCgUNDt5KW+ivocMokmN/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/s5Bf8G85v+7Jt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/vB0b1w/PbgxN9mDTX+5mZ/xljCtEMzmutvR/REDACTED/REDACTED/ioYHyelcKqdmpnyafqcgl1mpDhLX4/Fuh3g14d/REDACTED/bB7JWgQwqgUx7KFCoxRH/REDACTED/REDACTED/IQCOzUpt/REDACTED/REDACTED/xAZnSL/EWgThLE0HwtsHhRASQGhtUC5K/5ifdaVL+pY4lJJ/REDACTED/MmQDE/REDACTED/REDACTED/9vrK/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/9Pq9AsL5j9gJ1/REDACTED/REDACTED/V8EuV8L/REDACTED/Knt++QcmaKQ+ZFmK7o80P6vJd+Hp+U0mT/arKfRlP4e6I/nceoapGoOLPX8W1UXLr2tCets/BVZjKd5wwdGOSkaNS+yxhx7/REDACTED/AAAQAElEQVQXmW6KEWY/p5sC9zrbPDR/o+NCYgr3s3PQ/6KUEfd8P/REDACTED/REDACTED/REDACTED/140nYm5/REDACTED/+iXmWqt/REDACTED/REDACTED/qtDEQNzI/C/REDACTED/REDACTED/REDACTED/REDACTED/MVXQkWkOoi/REDACTED/rqmnT59evXz58spqUgAzsSGXX/pgX/REDACTED/P/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Z/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0IF9B0e1hMpq9No/REDACTED/REDACTED/REDACTED/q/REDACTED/ugoe0iIQWktxKqd2bX5/REDACTED/v1Sr5sGG9+9/REDACTED/50D/Y0LysVq5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/af9sDbrW7VMZLrft+63926Q/REDACTED/hsGOPtRpVgZ30r0/REDACTED/8HG4/qsP9mcxwtfJfLTvsjJ9Bdwe3IJ/2U4vKcYLf/REDACTED/REDACTED/REDACTED/02PimWZP9n26NPM0yn6IF03KHcDMz/H+T6ICr4o+5ZRMCBIptvzx/REDACTED/9nJdTj0rKJy86ihY4PnSJ1E/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/6apLIIOspvtHRJj/Lpe7UnNmPV5STzFqLdF/REDACTED/REDACTED/7PUqi9SOLBJ8V/FavR/r/REDACTED/REDACTED/SnexzEKF1p1VH/REDACTED/REDACTED/PlM/REDACTED/ZW/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/EBaj9/kwpPx1OghQeR8SyeGWpjTylJ1aZtJp/REDACTED/REDACTED/REDACTED/GwokBGw9Px/REDACTED/zckqyydHf9gfMKA70jp4drj/gPyUU54Kxvb/REDACTED/alBaJ/REDACTED/REDACTED/02vBf8QnUFIDYPeWp5X9UVbp/REDACTED/0lPgczX+W9SCY2BDweWrDm/h3EeV9raHJqqnGudURctBd/REDACTED/5s5m0/REDACTED/REDACTED/REDACTED/FfuGYWCZGw/REDACTED/REDACTED/REDACTED/qZQs9nNiIvQy5/r/ZoKnuX5/REDACTED/REDACTED/SlJw+nSJ+UVs8Jn/REDACTED/REDACTED/REDACTED/REDACTED//ZSD5f/REDACTED/REDACTED/REDACTED/7/REDACTED/REDACTED/2IDtZUOHp/REDACTED/REDACTED/JlfWLzxxE1y6rMKArjZGEM+zHUE94/REDACTED/REDACTED/REDACTED/u6GlO/REDACTED/REDACTED/REDACTED/ooOVVhmBU5p9yFFsgBXO69jLg/REDACTED/REDACTED/REDACTED/REDACTED/fePyI/bq7u/vYHz4xHAyb2dRX3XHjkcMHSzyZpx/REDACTED/REDACTED/REDACTED/REDACTED/PG7d8KU91io/wn51UXCscQtkqG0xJ8UEbMqhT/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/w3k/vru8G8UvDlpY5Rk35Y68/REDACTED/REDACTED//M3MiGB/jIR3gvD9SBN/REDACTED/REDACTED/m/SCGkCPPuBR/EZrA6WBH2jJ6jn+GzZ/nCTvcKjAzzR9/04D0/945/yHX8zM//2t/6h/+2saOf+cjPDwZtlPXkU8++9Wu/b1DNJk3Hfq7rf/auH4rqr49t99a9e02tBY1r9MP/+C9909u/3Nq1ubV962vfXs3Mc5F6Z/vDv/NvT98kZ7z/51999Hv+2g/hYOC/NDOon/vDd2b0ue+L/REDACTED/3eTx45csC/cvyerxrOLta723/4nnfccPIoTPH89f/ln//Uf3pPdjL54uyhU+Hk53DqFZ//THLTrxx/REDACTED/REDACTED/Lcc5WO6h/VP8tjsl9d1ArAXZ/REDACTED/qLIAkD2J+94EAlCQZxlRVM0/ck1DmZ2gS4DNCp9l0Wgalcpw/oGPvfiVtBdxDs6tKf0SiQ5HAsqsEE6Pu6A/REDACTED//J1935Jx4oIrr6wsXHf+b9f/DPf6u9Z8oTKeDRWMYv/6FvevXXv6n47hO/+KHf+Ms/PRjMRHrV9ekvveu/f8d3V8MqK3z+j178+bf9MG2Rqd9G4h7+x1/7uj/7Zuh5dta3P/2fPvSBf/ZrW+c2/daVUb3zpx/REDACTED/REDACTED/REDACTED/5TGN1/4GEleRC+r//qt87MzszMDmdnh3/0xLNNga/40jfOzzdZwyb/zNmLA+S9RhApZn/REDACTED/4mGQ24AUi/xB/a/VFF/3VW/plvhTf/REDACTED/REDACTED/JzNq4TLtTOs9/REDACTED/iqQvmv5nf/YuMo/REDACTED/gJYhbiUNatdXvfab3bpOG/dtBw31J15PCcWQqKSpJEA7Q/REDACTED/REDACTED/hf+6Lf5tl/+sgX/o2vkovWubeETWnh+MKf/d2/1Rf9Ns9NX3AXeskjevW3PvS2n/jebvTbPMfuPfVtv/t35o4vJFw59plZnL3/W7/oz3/kH77qmx/REDACTED/REDACTED/REDACTED/wojO5QZ446LlcGKI0e9cMgfh46VR/+wzSfR+bc96FQlxtlJ780y8Fu+Kuemxu+9/c+wv37H3/xt3Zp9647Tj36u3/Agv+j//REDACTED/eKvvjdczAij0egDH3r8+NFD/REDACTED/bNMaIdppi2broL3rjve/85fc2SH3xI6/REDACTED/REDACTED/REDACTED/TAvpPly0VE4S7hK+KEt7/nBmHUktj40qY5cl/Ib9PBhmg/REDACTED/REDACTED/REDACTED/O3D3//2858+DMw6aF6tDva8egM5vBL/tk3Lj97vvmv762NC1caSzwYiQd/9P4b7vrqB55776fGVPTI3/vaX/veH+Oxk+ati0+cGV+en7u/+sHP/MbjWxfWWb6Idl/REDACTED/REDACTED/REDACTED/Zg5oWiQ/pyWNyHa2pEVM6phcjictT/REDACTED/REDACTED/REDACTED/6iB//RD/REDACTED/9av371vMvvwFb3zt3/pH/xZn5kwmYQuairIA+PChA7/4a+9vsv7in//REDACTED/fuYX3jWYmW25LlS6OHvo8IGbR/WoMaXh7l8OgPnuX7vR1+7+BYp/REDACTED/fchutM3OBghM0dj/REDACTED/41/k/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/J/fNMNn3ebL7+5vD6zODeYHfjMj//REDACTED/REDACTED/REDACTED/rPpk4BT4uX3qy4T1sS3xyi56v/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/tXv/YZ/8AM/xQf2ZL+yVEgPETUzvd3ot3lmZ2fuv/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/G2m/REDACTED/REDACTED/Th3/0Xb/9N3/REDACTED/ogv2YSmP/HI31t+5iz/895v/MKv+JffyW1jgZ07tpBFvz//J3/ws7/9eAN862/8nVOff5flv+n7v+I/f+OPYDXs+hm/+C0//Pz7Pt0A8wcX3/5zf/REDACTED/qT/rlVDkE8JnLpO4wvlBM+1BHn8Qhq/lPJVyVgc5OjniKjWzLIqm+nV/GTSLq7DdREcuZhuokBnhk3jR/REDACTED/REDACTED/hV/36tve9NB9PBBz7z23vvf3PsrkfPn8pe/+tq8+fvTQ+97/EW7k6pX17/2Or0Uc/Ow7f/REDACTED/KknP/REDACTED/REDACTED/slneHtKcMRG7/29j8h9s66ue26/cW1j6/c//IksP6jFxgvarut2GfaRQ/REDACTED/REDACTED/REDACTED/gfDmwuQJ/REDACTED/REDACTED/REDACTED/REDACTED/Hj25eXrPXP/nzH3jmNz5265e/llrz3rbxzq98yNf1wu9++tnf+QSX/4W3/+Cf/Nnv885StTAYbbTnhF968mX/1tblDX6libd//u0/8Pb/+D/aTy2C9a70HY3OfPgzqy9dsl/HmP6GB2uqp/Qbx8JuG2C2PdAFgQW/REDACTED/BTY07CuGx7AYekTKvKToFTKnE/REDACTED//o+z/REDACTED/REDACTED/6Tvffr9O3jaEXV/feP1r7+F/3nL65L//REDACTED/5tq9ZXVtjHCxTe3CAg9mKtr/REDACTED/REDACTED/REDACTED/REDACTED/fqIYjpIswuky03R5/REDACTED/REDACTED/vK//REDACTED//WJiq2Fz/6735nY/kKtMHksKoGu81bRBvLa0/84ofmFvY1pr8e7dz7zV9w8vW32Ct/8K9/sx1JGcw0gr99ZXPp5AH/wRvfePuZ9z7T8N7hu2/REDACTED/UI2S3nog/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/w/f9+f+uY//486zCy8ITFgXb/q7lvtpw8+9rHllSsWAN96840tw0ZUkm898dSz99/bLnx66yMPbW7x/X3w1Geev/fVdyTVWVe7Z25x/8xwPukYY6PhkPn/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/4eatBt5aX3n23X/kA+D9pw6/hJ/tUrb52uLSISbL9vYVH/REDACTED/CO//REDACTED/REDACTED/REDACTED/REDACTED/3P2Y0+Yn/8CuXLl953X13W86D99/54Y8+ybKTnQL9zv/yO2//6i8BkHmXM2fONekv/dqjb/vKR+z1um7t74h23/+hj/tToH/0B/REDACTED/k9chIR/REDACTED/EX3UcWFWZAxFbh8p1UwqMWrSEfcnCqUhh/WisOMa+Ph/REDACTED/REDACTED/REDACTED/REDACTED/42B1f8VpvEQYLs2/REDACTED/D/2VP26ro5tvrj53oem18FbrALz0oXYJtLXrS3/wm43/RR7CD5/REDACTED/VwYioz/s7EHrP9fOf06+WfC9vX+e+O2p/dVTohL/REDACTED/REDACTED/REDACTED/5d7/wzl/6rQaXH/rH3//wm9/AIve3/8G/+PXffP9X/rEv/kf/y19kTH/73b//P/REDACTED/93/+bv5n9/1Z776X//kL39BvgR6th1FhnbU/3u//e32btPLH/34Uzu7ozd/4QMW5a6sbnzX9/8ADIaN7OB2cgr0D/6Ln3r4ix7Mhir+93/2b3/REDACTED/REDACTED/5VHANBvAHb/REDACTED/AqjUL/REDACTED/jEJyHD2w0Mq9HklSfso/REDACTED/REDACTED/REDACTED/5us/P3/94Ve/7s88vLO+/dgP//of/pv3DUYz/REDACTED/da+2n5suDmZlB+0rAhGh2ae5Wt9R5/REDACTED/REDACTED/REDACTED/VTdB9iSO4NrgeVL/REDACTED/REDACTED/+/xH3HtDWZldh2N7fva/+dfqMNCNpVABJIBmBacKAy8JFIRCXBC/REDACTED/jJJPo/Pvd+5X9tln99MoouUd4PDIeLfP0od+9ePjf48//iio/f4rf/37x5p3vM0V7v/5Pe/m28b/FsNekdTwP7dO3IIAh+Z7pxgDUOi/fn2DOLAGIIIKllI/APMl9co5dgo18l9sIlFrjhH+3F/6v8rZm/n697/REDACTED/vU59+2iq//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/99z/BgEIav+a+nTZ4i6NLaC/uOz9fEp/REDACTED//6Jv/0i/+zfdC79o73v+Kb/26f+9nvmPvvkM/REDACTED/REDACTED/+sjfe97mvaqLfn/7v/8HH3/N+SXZNH+tcku9QsqiiaGD7N/REDACTED/REDACTED/doTH//0+OcL166fnJ6VyoXubwz/REDACTED/REDACTED/vXv+/w3v5Fr7r1y+C9+7pc/+sSn+MMf+OATo4szFF00OkEf/fivPfGJT/OdP/8Lv5K3oAD8m9/97nFo1xA9PFiM3VF0WfJdoBFffOnGd/2df/hlv/4L7M73f/Cjd+6c5vnYWpPVGu8C/XO/dO+VS1v76Fc/+vGLB/etVyc3V7cT7/ycF63J5Gf360tVrJE8K4Ae/REDACTED/JDv8V9YO8Yhb/REDACTED/REDACTED/KmDz/0H/31X/hr7/nCb/5Nl19zn3KdKHqGf/N/97v+yR/REDACTED/XOntlfOcLN+M7n/REDACTED/syL0/REDACTED/REDACTED/2jC7/jt3yZzcX9R//kx5f7h/t7y6//HV/F9vbJp54bBwH3j3IEtRj/REDACTED//QT/yRP/h7uOa/+bY/9KVf9NY4BXrIm3EuYb3+ut/2ZV+tNB+v46PDP3YrZ3+/6svf9htC/b/7u7/2r333D/PCrrgL9L333vehj3ziT/7xb7I73/Pj//LCxUtfFZ7NXhHvAv1F1S7QP/REDACTED/RrH7v/REDACTED/REDACTED/doIvE9RriKobRMpo2tMUVWuUFyGPLK/g56cebm89gB/REDACTED/REDACTED/BvXB6+8aT7/voD/6Rjz78hY9/5bd/w+t+8xdMbcc7/6uvf++3//REDACTED/qnnSvJiaHaB7l4f/We/+OJHn9o/OC6jyvmN60TNLtA//REDACTED/REDACTED/j/7cqV1toel/REDACTED/9kP/Nmpj/tv/Lavev6JfxprxtjpxU/86Aj8wLv/+R/6E/REDACTED/J3de0t99/7k++7du36lXHEFeDrfsdXP//CS/UtyI/9rq/7qlj7xV/45vE/mFxf99u/sgTAUH84OzLv/qGfjDV/9+//s+PjS+23PFjy6/f/REDACTED/IiWxJlatWMHMlbCjImEflAYMCJYOkGOGjLMIHW208Wx/REDACTED/2t9OTtcfEueFj8s8PhwuP/REDACTED/9vpHgxxhDUN0r5SVsd/REDACTED/+39ZHu3/hv/id37xH/2tEK63/REDACTED/nJtE5v+Xe+Qt5Qrq/9X7/pI+/+xcViOZVHu/7Zt/REDACTED/REDACTED/REDACTED//REDACTED//yfdV3tS26yNPfGo1suY6wV1dW/qxrj85uZV3XEzrXDptsb2/ywPn5CXY7Z5pa/IGknEX6GvXR/os9g7+zP/81971tb+BK9frlKdAl+v9v/REDACTED/REDACTED/REDACTED/REDACTED/M0QoYTziYfByIbfJnRSya/REDACTED/REDACTED/REDACTED/REDACTED/wTS5VawGZrSRjZEClL2Mt/REDACTED/E/cu7t2XJ0JP/REDACTED/j2/+Dd/4jf/REDACTED/6F8dh5OQlheW61unzNu8Et6nOgN85mc/usr7ROcR2lj/L//CDz/zS598z7d/z9d91x8elh4Dv+nrv/DDf/REDACTED/REDACTED/REDACTED/REDACTED/PCEpfLw+X3fv8//e//1B+b3v/8i9eXi71RvO65euldv+0rYbfrc17/2BOfepZOKe4CffWeK/REDACTED/Nj+3lFZ/ZsnP0OOT/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/XZD3zq3jc8dPFV99iTD7zlVc//0jOleXjldQ88+AWP2U/v/PZ/84f/6N9GPQTYrrTiTVXy7OjxkUe+6HH76U2//e0f/r//NXfsGFi//Q9+zeXH3FL/zP/0g8vF/REDACTED/vJ3/9S7/vK/b/Wv+vVvfOIffyvoXrtp3e4Cvbd/REDACTED/REDACTED/REDACTED/REDACTED/8ThQY2flLXXKuZkjs87/FyqC7z2EtfWLjIjrTSQoSsIksf2k/REDACTED/LT7/2pnx/hN7z+0Vc9LPsZPv30Cx/81Y+NlvcrvuRtXDOOQP7Ln/tlhv/hD/REDACTED/+NI42PuWz3s9TC4qkeQ3fv3XxMpPP/nMM2FL53vuufyaRx+2P3/v7/wtf/p/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/N6RW+Dw8bpUDNcvFHbpNVyu8DeLRUPQeR/CU/J/REDACTED/REDACTED/pHX/0Nz/2VZ/zo9/yd299+qVcNeD+wYW9/eOz1Z3Tm9dPrt++CB4Av/TJ54UHcPjl7/6JB7/g99pPb3jX2+/7Cz/y/C8/7T4Jwf1f+Kq3/rtf9qP/yfdw3z/xw/86BsBv+X1f/REDACTED//3t+6jd8x791+TX3c/2YfH/HH/2NP/e//REDACTED/X+yLRwfm0Aj/REDACTED/REDACTED/REDACTED/Z7/ePzEt/zHf+BrvvKLmeb/45/9m+9577/8ii97+7f9iT/INPzpn/lXf/p//D8Y4eXe4XL/REDACTED/Yi7QAO88NL1RKuxdnlw8K1/6s//p//R7w82KD/wgQ8+kXdoTPjqV92vc5Vz/R/8D7/zqad9LPfy5Yt/56/REDACTED/+0v3Xr1k9W9502PD0lcK7Q0HR/REDACTED/yrzAZDVjNHh4tLe/WD3/4vjIUaJbZWv8oO/REDACTED/REDACTED/REDACTED/REDACTED/6H373J37sA7/03f/i7KVT1m9jnPmG3/qOm0+/NP4nX1unW89c55N7R9ze95d/7HVf89bFkYeUX/af/fb3/YUf/czPfmx9sjp+8OIb3/W2x3/r2+48dzNPMU75iz/753/o1e/8nKh13/D1X/Dhv/++g6sXvvxb3xXnOf/REDACTED//4D//Vr/jPv8F+evgdryVcUSoxCq0/U0+Bvvy6e0amgt51/RPP5u057tafrOUXO/REDACTED/REDACTED/REDACTED/67f95+Olf/BN/3Or9Ijav/a3/REDACTED/NF//jPf+zf+u4ODav728y9ez3tUpPXv/REDACTED/H/REDACTED/83X8RZq5v/87v+sc//REDACTED/81o82/REDACTED/k6Bzafiwk3bQj/t6khnve/REDACTED/REDACTED/SVLCMUukSMqFtwUKsau43BoZUUu2q/jpWEMykDMdpiJ7UrO8LC/AoW73qaNH/REDACTED//REDACTED/8O/PFsz4dlXhOMy/REDACTED/lv3V26/TFJ54+u3ny8Dsetz2u+Hrxo0/ntMFoxAviI1k/8RMf/Orv/D3xntd+zVugjN/REDACTED//cH5juOP0j3/K3xgHbYXwqpWYX6KMrx9eHayMG+0cXP/kTH7z/8159/IDvf/nFf+xrf+5/+7ERt3WCR+op0P/eT//XMHO9+5v/j4//kw/REDACTED/REDACTED/6rg8h0ppcafY1T4AtbD4U/REDACTED/JZa/YtvKAcgHR4dP/KQzJ95+ukXTte0d3D8FV/6dmVZevcP/+R4G//HCWnjXPsfS67/REDACTED/PsAIW8vJf/pTfcmXB9w7OPrBf/pTANMb8PPe9JrDEBj/ygc/ttw7MCKP/REDACTED/H7p/REDACTED/REDACTED/nGwKDuIAlfsHU0NCKf0kcKd5j/REDACTED/REDACTED/REDACTED/frAFYAV/5H+BxpCRSbYUnpnBBjmymaO8d7x/gNvffRVX/KGJvodr3/8h//KOPRq5mJ5cPSz//sP3Yi7TOnVPGvCstg/+PHv/D5LvMivk+j3/jg0DgAAEABJREFUyZ//2HMf/PRyuSfcNLm4VcvFwTgc/eN/6u/Gn774P/REDACTED/REDACTED/EyxhXDtjGm4PBQ4hVm7h1wE6cW+BlWm/REDACTED/REDACTED/tcXgk8Xj/9M7+43NtfLBYf/REDACTED/N9YOPG4d+acQIICSsmX/SB9pdoFfDWc7GDcvlt/2pP3/vPZejfXn/r3z0bHX6pe/43LhX8/f+3/90cXC0KEpNdkVeLP/qd32/b0gD8AWf9/REDACTED/T89clf+/REDACTED/REDACTED/REDACTED/ACJypbAzY7ZpSf/REDACTED/REDACTED/REDACTED/REDACTED/9yHPs0TjE2uuvAHvvenP/0zHz04vsyJCe6vkQ3+0tv+5Du/9Rse+ZI3zD1757kbazqDVfksDk//0if/xjv/y9/4p79x2Ft073/u/b/2Y9/23cu9w7IfdbaZz3/4yY+/91fsntsv3hpNO3PWYn//F//2T77p33jH3oVDe8/r3/UFH/REDACTED/REDACTED/xUOz/H+GISQ0V5j2W/REDACTED/REDACTED/obfYpNm/8bf/gfjUOQ7v+Sttjv0D/REDACTED/roqx40nJ5+7sXFMPyBb/wdn/+WN1rlt3zH/7q33AeepVb4ZEj0U//iF7/rL36n3fOaxx7+s3/1++Iu0BcuXhjGpxADPrS3t9fuAr1/gGfDl37R57/q4fthh+sfvPtfHB3dKtthlpO/REDACTED/REDACTED/REDACTED/REDACTED/coYsz7jNunzAe64Mv/REDACTED/p/rn/quXf8ka997Ve9eToYO15P/cLHf/iPf9eTP//E6CCVTaTCZ44v3rlx7b3f+fe+8Jt/0xgGH91/qXn29MbJz/65f7Ic9obFHj+0f3D07Ps/9SN/8m//nu//E7Z/FV+rO6sP/L2f/pE/mU/REDACTED/48V/5jX/mG+2Gh9/x+Ie+/31jZPHIO15375segR2un//REDACTED/Oy3sA9fhGGNpIs6N/n/REDACTED/RqDNmO/REDACTED/REDACTED/REDACTED/3t8+37b3+rQe8lgKby3NrRDXvzhlAx/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ReeeOaFD39mHH09eUls8fGl+3BRjoEM/sZoXtcrHo8d0xmLh97+2ke//E37F49eeOLp537l00/9q4+NqeqjC1dcI6R0+8bzzIfj/a/+0jc8+hWfd+PJFz72nvdf/6TshTm6CoeHF5UP6fT29dXZibVl/REDACTED//weG/REDACTED/REDACTED/EJdAIz5WZZOgbXHSr2YLTA0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED//REDACTED/REDACTED/WqbXl1N/REDACTED/i8rY/REDACTED/mUKWlP34ta/REDACTED/REDACTED/REDACTED/REDACTED/2e11h+tQ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/M7Di8/REDACTED/REDACTED/Br4TCi5fD0/REDACTED/88vs/wJ967N5ft7c4TmPGO+/REDACTED/REDACTED/REDACTED/tJ21XyJWpnbOPRUSOCfpCdrDsGOtO/REDACTED/REDACTED/aXl++//REDACTED/REDACTED/Ive/REDACTED/uKIHVhDmJA26lxE/REDACTED/bd3ESRuNJAvZ+MiaWNXB8TN9R/REDACTED/REDACTED/REDACTED/REDACTED/diKkie+j9/66g8XRmtYlAM4xcIIyAkw86ksk+e/REDACTED/REDACTED/MJ8yK+KjTYMm/REDACTED/REDACTED/REDACTED/SZl/REDACTED//REDACTED/REDACTED/u9r3ADf4bCnv+trh/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/6gEaL8zbERhe/REDACTED/REDACTED/REDACTED/UB2ODpN3wzVxotNvkDU/REDACTED/REDACTED/REDACTED/DPi/ffuP/fCWd5HrRx/hHu3KO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/TLjZlg+3e8ixNou9uCYGHAbY/REDACTED/Xf0k+I/e6WYKTmCRchSZ3eA/s5VPShLY5J9XujGxwEz8/REDACTED/REDACTED/REDACTED/g4/REDACTED/REDACTED/REDACTED/x1KDxHAmbMNEMMpi5XI0i71/N9knw4aqFlgVReR7vRFaGgkRCCWwRN/REDACTED/kB/REDACTED/REDACTED/UwsAnN1B4MQ4vlhzivvWSsUZ2/MNm/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/T2Jjisoo8KAlfNLh8lJ1zy7RD/REDACTED/wNTHgB08kynGsM3/REDACTED/fkSWxEZ96n/zz/REDACTED/REDACTED/1aTASEjKBwELl76BEf1E5/REDACTED/Zs3StV3sU1pdwErhl6I4xzwSTSFqFsu/REDACTED/REDACTED/REDACTED/REDACTED/1/AUwbRz7GjUxByHGi/yjO0TcDb/REDACTED/yT/MssNAEfoCKT5JliGv+AUW/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/vJowY08Sacu2mCRbirHUZa/REDACTED/REDACTED/oR/REDACTED/REDACTED/JbMZW7KzVvXbt66LkoVtIx/FpXKlawMUX9F17ZD2XR/yKEvlrnQuFji3oeffm+/REDACTED/REDACTED/REDACTED/REDACTED/BzMpklogdy9b/REDACTED//ld2B8gRk7R4L8Vcr/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/YWVU/6pxoEMPGd40EPToYTk/TyQmV1b+rsuHzgHu30/o2kXKFqI/REDACTED/VJzJ/hwK3G0epwyqnnpKN+hYG1S1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/HD/WljMmdictN/REDACTED/dXjnUXn23yEtQAbLx2kF9nKxfmCSE692///Dj8+/CVtyTKk59L9LvWrZ6lJAlpSQ/ntJCYf7Ag2VSSTRqkN7z++MLRYhz75bN/REDACTED/9oYSTdZtCN6+XcJBatFX/REDACTED/bJZo9BZXSsJOwsyyO/REDACTED/REDACTED/REDACTED/REDACTED/XCpvvfia8qvpANwokPyDaJQgoYDrZZ/41elWnsFHnpg/REDACTED/REDACTED/o5I3OOHrpKj9ix3XcW/REDACTED/REDACTED/REDACTED/2qomSDETeBscHG/traE/REDACTED/REDACTED/mx8Pbp9D/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5QCQ7GukFN/hQWcqrqRm4w/REDACTED/H89d46Lodw05G3/smJejOPAl/REDACTED/GmnGc9CtqJgj9Z6uv/REDACTED/REDACTED/oOVg8EB89i/REDACTED/REDACTED/LQUVPGvmY+dSNYouKnLSXGDaKHh/REDACTED/4I9JTZ/qC215JZEsmJ9bHsvA8ciqU4/REDACTED/REDACTED/6dX35WjVy7YvsvgFnYN/i9cuDCWt2/REDACTED/REDACTED/MMC9kryE4NOCfm/REDACTED/REDACTED/REDACTED/tNkTK1KEeNSt77/A8FzpNYhhcnsu8tuZUUkPIsS6wPKr/8VdiyBJYcOZYBLD/REDACTED/REDACTED/REDACTED/REDACTED/ZLlZ5xhrI6qugmoMkMet+IVsz/REDACTED/REDACTED/bPwiuaABcQ8/REDACTED/REDACTED/Xrq191cHgwxrrrsv3VOq/REDACTED/j9u4Lagy2Q6Dh8pSrzvQ9vL3/REDACTED/Jz6vsFESzisUi/REDACTED/lHWwmjzPXjEvAGbfstD/REDACTED/REDACTED/REDACTED/9/2a2qdiRXeILk3eX33PHNeA2vU+gu4u/NshLjPu2MrL20S586Dp/B7jsAj2Zsxv5/+VIUF1Ww9MUp/REDACTED/oZnTxPnY1UegWYEicz/tpXdpRjRSutb4VK6ieOmr5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1SJw6/REDACTED/ITFyMqxoXOxtHnnm2StCnysHO43EGsGown6/REDACTED/REDACTED/2Y/REDACTED/REDACTED/PvAKtW/l/REDACTED/QQ1Xfo71daGeul/SzXX9rNAy9QgdjiVaOd3/REDACTED/REDACTED/XcCt5lI3mh7O/REDACTED/dvn0dwqeVywILBwi9DzB4hhIiK/REDACTED/UvnMLkHz/s9UXNB0PphY1H5XKKHjp0X/zWaCOLtt9w/REDACTED/REDACTED/REDACTED/REDACTED/2XZU+To6Gm6f0O3b4/vOygLH8f0LXF4meKrs/REDACTED/Y6qt3cq/REDACTED/REDACTED/REDACTED/REDACTED/w19Y5eQb+r+gbXb/ADWzm6Sz9zNz/WfK2wXshOZkMM/REDACTED/KebEhW6EbbxC7cRNSr3eCfvC/REDACTED/jIXYBCDAfNA+VLtAD1tC+nZe/REDACTED/hgA3bLexq7pqLPwVHeiqPigy/REDACTED/ziheMFpfHdq/REDACTED/CgsX4kW/REDACTED/tEIqhijjTtEoMBjIDIjQV/SSJ/REDACTED/A95v1Ab5A+Dm/REDACTED/REDACTED/v3nx+dlXhvIUAlk48/QzP199DdQvN/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/UZGN7u2ZGun/Tcy/REDACTED/REDACTED/REDACTED/gGFsW6QEggaRclZlnJ/REDACTED/REDACTED/qkCvUGM0j4zV6BdvGWpflNnF/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/LfKpjdwbWq29m97EfSdgAqe/fDx8uqN20/Jqb951LeAxWdmh9viXpV/cwpLDZmuIFE2+tUHjo+ee/REDACTED/REDACTED/REDACTED/REDACTED/TsNkZSKBbl/REDACTED/WyAk1Dmruz71E/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/OZeG2cYW8wFBQAwmPVrXhd/Atx4MnTwABTmN3S70komvs+Zc/Zn+4UxmGairqXGO/REDACTED/CFQZuHgiImS34Jr/LbgryHA6hAXXwwWNSGijjfb/REDACTED/REDACTED/B8E7H5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/RW4O6djZuBG3Tmdzebx/REDACTED/REDACTED/REDACTED/+Z41M/REDACTED/eI4ma9USop5ChDW/g/3gVEdjYPvKB3CnM5a0N9D7+/REDACTED/REDACTED/REDACTED/HOt6joq9B6FZcfDSrLUos3X/REDACTED/1RgF/5Bx/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/DvC/REDACTED/CGakYG4ERmGeKOuSPiW/REDACTED/X6lnu1WOjj+TB/qCnRSGmG4J9ITofIs04zSIZkwov/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/oo8RbNsvwFKbao/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/S3lq/jbU3om9awAhe0dA/WLnjqs6Yeuzk48B/REDACTED/REDACTED/REDACTED/REDACTED/l6OXONHe5B9InNmmHUkr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/RpKl2V95wqLAxl8ynR/REDACTED/S6QQ9VwPcL5raO3lI/REDACTED/REDACTED/REDACTED/REDACTED/cPzC8y/REDACTED/BoQGfcpVU43n9Uiaq6Z48BMU2UiPbDq9AV/rOXn3vtBtE3xtamaAipjM5qP9+M/REDACTED/sO9mMy/1i5Nn0x5C1edYmFqzF9Cn+uAn/YYK/REDACTED/REDACTED/uYetvHonEHBIbuP0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/W80o5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bztrUjV+pX/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/W+a8y8C/REDACTED/REDACTED/REDACTED/t7x4/dZTo1rMeeW0Lk+Vyc98/REDACTED/REDACTED/fPdB+Bf1RHoRJWNe/h4xW3Qc2+TXxhd/NoRnyWn5mdTYlqZF2/mV1IGnbV9/REDACTED/REDACTED/REDACTED/Lpawf3L60kZ7Z/REDACTED/REDACTED/5mPwjxo/MkKs8EYR32pRsQbrwdpl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/hiWeTb8k8oxZ/eaekEqjCWVvNIQj70wAU1E8H5/REDACTED/7/REDACTED/eHJ2Z/REDACTED/REDACTED/IieP4iTwJgnStomc5ekSAo/lB/REDACTED/REDACTED/W0tn15U25PBFQt6V/REDACTED/REDACTED/g7ghaYTrhwDZMOzq45+Erb040qjdZ/ctmGAQW+8KwbLQAYmDEW5FMs3vD/NsbX3/REDACTED/REDACTED/REDACTED/e/njavGZrEU5xJ1Mg/REDACTED/REDACTED/REDACTED/REDACTED/SPV/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/XEZfWfatGn13YpDxYQmAeV/REDACTED/REDACTED/REDACTED/elRYImvdJeRB3XbbdOlN/Dx0rTXCYFVPMnG21l/REDACTED/myVXUIoXDsfHsxIf26F7/REDACTED/eW+R5z/nyc9Zq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QZhU72sKEiYGo3NVvK2hrCg41/REDACTED/REDACTED/REDACTED/brBLuRseMRt1QlIasHq4KzxLrBD/QwMoXJraIuub7ruS+XKbLxwF1i/REDACTED/REDACTED/eg0VdoAJ91NgdG4ZszUKr5Uea1/REDACTED/ZJiWBoEpk5jiQMDMmJa3U/ck6g97F4ZgpwOgNzzNT5sXLU/REDACTED/REDACTED/IcUb+MR0Ox2lxzyrd5hXC4/REDACTED/REDACTED/yCYTqOQoOJYyR/u4zOPeS/STZzQY03PVgj/REDACTED/BjscbzaCqp/REDACTED/REDACTED/REDACTED/Gri80uCYAs/REDACTED/REDACTED/y6xeLw8VeXvd7emdVrKPu/REDACTED/REDACTED/REDACTED/REDACTED/tcsRkw797/REDACTED/REDACTED/REDACTED//REDACTED/i/FGqjUD2o/REDACTED/REDACTED/REDACTED/REDACTED/7yLFiQObGyuxaK5QCxe3aakUQM/REDACTED/X+a+At6Oo95/REDACTED/D9vm24me1ZGf/P7/REDACTED/REDACTED/REDACTED/CZk+AniLD1YDz3kiHerLBo2QD/REDACTED/XwL9/pH/Y24Ri8lF7Pa2iL3oD/PVrtt7WfM/REDACTED/REDACTED/REDACTED/REDACTED/fuG+wIylt2K9/REDACTED/G9FIlFLd69k0OS3MXa/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/6BPerJmP9Yp8b58Yk5YRU+wXPsSnJVaY9x/REDACTED/r62lJavqNfAlCZUsKNmjRI5RgsX7KlZRZZk/OSFBgckmpEULwu6Uwk042njYtI/REDACTED/xsvKvM0eWfj8xFjB/REDACTED/REDACTED/4a1T96zgCZSyxgWPl/REDACTED/REDACTED/REDACTED/akYZ22py/wXF1oVsB30f8Cc4th/zgNsH80sjBTPE/REDACTED/REDACTED/REDACTED/REDACTED/HOTCy/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/l9huYc2sWz/Nh1k1L23X5zcDFFVCt0ZY8wca/REDACTED/nH4mCSFNU7dZeRPXQTgpnEgRZl/g8ltCmb3tgkh4zts+jfE5Gax/REDACTED/3/bPkmSikv/REDACTED/REDACTED/fxFK+JYmhpu/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/9/zhPYPidPE91/REDACTED/REDACTED/rfrrt0KE94ZbkhvDgUV9KooK/Ap3EOF8BaYP/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/vV6zDnpQEwVGhjkBPHdi1SdWn3/249x61goJbb9/REDACTED/REDACTED/f8kLX/REDACTED/REDACTED/REDACTED/xjtpYlA7tQRBYMmaz6iq6D0Na/REDACTED/REDACTED/uho+UQqtLL8YtR72i+c9mvv0oBAWABz8/REDACTED/HBsY/ByLJjSbOE3S/REDACTED/REDACTED/REDACTED/H9WT+0H+z/REDACTED/+b6p/REDACTED/REDACTED/xK/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ppcX5G/UBbpJLkBtUpIk62XK/REDACTED/DlD0fQKtlZNwMyneEhtD2QnH7TQVzJNKe7/REDACTED/XZF1iZCCm/REDACTED/REDACTED/REDACTED/zYC7fi6rYXDGVK0OYqg6tkrVZF2Q/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/uM/Tlq0eJGyMhApzjnn/N6eeUjqGZzA66MU82nuIQ/REDACTED/REDACTED/HzyrZS4rfYa/Xw9royMYPffi01pZW228Dmwf++Md/REDACTED/REDACTED/FEsTxUCyuJ/qzVq3PmFt721tfRO5lU2PmA13/REDACTED/KS+eWRk4Iwz3jBv/jy/Pl//2o+6u+bYkOLxgWGqiEOioqHhTZ/4+JldXZ1+/REDACTED/REDACTED/oQAQiVKBKQnG+SpjSwgVsKIO/SVisBxVMSx40DZlEUY5AkTF0muA/REDACTED/4elgWFWgrtQi8ibMaP8NXLIgy/REDACTED/REDACTED/JJrRLIsYhBq2mXpBG/Ny47CyQbz5rQt34H/f/8h01g4POKdJRuuN7s/REDACTED/REDACTED/REDACTED/REDACTED//3Gd2WbzQv/r0U8/fe+9azeM6IhbvVPvOZqs1wZ/HZqGVJ3jXg9j9jsGIiQAchHOjiv/zna5/GLHhGsEOc5prq2On/QmfFR7TL9w7CZ5JovF4fy2sLtml/+wzT/dbPTo6dtnld/V0zYK9MmA2k+qMGATgmVd/REDACTED/REDACTED/WSrna3nZ3W0uXsDsg/KXR8hGH7f2ud/REDACTED/REDACTED/I8ppaWlyf+ncjiqboGMEE4kxD/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/gR3oU5rdwZBk1GzvpGeu/REDACTED/ywdzaEO9LuTr3sPet/REDACTED/aBy94E+/REDACTED/REDACTED/REDACTED/9/REDACTED/JhsFuBKV0nCYojcZcRux4I+xF/FxB2OxEMzDjCOUX/REDACTED/REDACTED/m9aUcgLXUIaFnyynVLUf8jnLwxdG/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/fsthCPzWl5r2BZqOwrYS2OD9913/REDACTED/KTu5mq8ffjtytrE9SNmvC/REDACTED/REDACTED/TCb/REDACTED/REDACTED/R9mBZptU6Rr0/REDACTED/KMeUii4ZFjAWKV8JTmAbSRj1ndt/REDACTED/qRJxqPRsrLhv40MbrE9WtraWnrWUGRHaoK/IBDoFyRkTqgHx6/sCCrxjAfNSRhyc0wH/682WF/REDACTED/32tjvC/wguMo7C/0d7KvmYn3yDHdYxkG9xKzvaioWikfc/REDACTED/o+PI2Mh/7r/REDACTED/e+Mjo61t/REDACTED/SDcBKcukx4h4o4QzNjZ/REDACTED/REDACTED/q9We40UqBpbT5BHg/9XkZ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/PBMOkV0nEHrp9pKxRe/9BZeD861bw9N4J/REDACTED/p+l9Kx//REDACTED/REDACTED/REDACTED/REDACTED/+9vf+evHF/oiuW/t8NrvArkUeBvPWiy76/UUX/cK/+b577pg1a6Z/BbntSHIQaaaHyA749CJWBuJJNK9hr4/v+0LYDTX14K+6ndfjEOxI6X+PjA0vXrLcf/SnF/zkVa96RexlQikm/REDACTED/REDACTED/WwQ/REDACTED/REDACTED/REDACTED/0YUi/OZXkUqZ47Hlc/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//lTNucOMi4YuN17FdUep16VFZvl4aH7rv/REDACTED/REDACTED/9OjOaK/f/REDACTED/REDACTED/REDACTED/lt/REDACTED/E/REDACTED/gzkIAI/REDACTED/REDACTED/h9XFsmRRNIBkzjqR5sJsHVdo70/WGz2Nhoso1vq3huoxzKElg2ez61ID39A/pza/0zybxeALioimL67bE2V7HYkuhR/REDACTED/R/+Vhwb7eouCLPT1SFcRl3kZkZhN/REDACTED/REDACTED/xv/vPamTRtVNl+oVyuVaimMatmM7t6WXL6VetehcOmhcBc/REDACTED/REDACTED/REDACTED/REDACTED/qDjLDlAPDNS/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/DqyeqB/REDACTED/8by0QgonjZ+v36ZZ+lbsQFVsIpmgES/REDACTED/REDACTED/REDACTED/REDACTED/d/REDACTED/u3DmauI+MjF59zfW/+tVlYBOUckjuOOx4CMwvNMbM5qovO/6glxywz/Llu82ZM0dXRr/REDACTED/buHCBfZDWhH5/R/REDACTED//REDACTED/LJb29v70bpJEb310liah6PR0e0H7L/REDACTED/REDACTED/j4o48+dtXVNz/REDACTED/REDACTED/mX7Zu3fbb3/REDACTED/v0oe7VePzt2rN9t955Xn/RK/yu//REDACTED/dfttTXV1kixuGlWx29D2nvcF/yYMPPXzN1ffuu99uH//Y+3bbdde2tlbdFXp6PPjAw9/77m/bu2ZngpztT1DBmP/REDACTED//REDACTED/REDACTED/dBDlr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/h/REDACTED/2jH5+/REDACTED/xxOMnqLQGM3/40xWdHb0S/REDACTED/tLjj9aee8LLjX9r4bLFY+q+PffLCC35kjB696x/REDACTED/1n9JX3/Cmt33n3G/uumxZ6jsff2LlL35+WWtb59jY0H//91lzZs/2fz3v/REDACTED/REDACTED/2Zgc0lDVmS/fcPgcnns3aedvP9+e/lP3XDDTfc/8PBnPv0xFLQ1vvOj//WlttaZIGqWepssFrd+9rPvmz9/fuOdz65Z8/OfX/Stb37Nv14qjX/2c9/REDACTED/rP/nJRc+vHw0gqWGtOn74Ecvf+IZT/JqsW/f8/37/d+1tPejzrMdl+R6zzjz9P2PzatPmW/REDACTED//f4f/vDXYa0gzUIwV8vjIx/60Fv22H25f+fKVU9e+NNL8vk2/DcmkdUz4Q2vP/aYYw6Pz5wtX/3q+a1t3Zrf0Qr5pUt7TztNT5WuSWui4dZ55/1q46ai5lSNIImkfubvoZGBH/3wy1oOMsEb7n/god/97poC1DDydOlkWMsmncJEet/xrW9+QgtK/Df8+Me/ePqZQc2nKegFhcSM1479e7S47eP/9c4999w9QTdSz/fd9+Cvfn1pIddNdouw6EdGBn7xi3MSc/vt73zPD3/wv/19Mxrf88gjj513/u/REDACTED/R+c/REDACTED/REDACTED/REDACTED/uVEjLbj+SdCYjk2ko/REDACTED/REDACTED/REDACTED/8W1trp22P/REDACTED/REDACTED/REDACTED/f/REDACTED/REDACTED//7+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/cvFnmsi2KHiDwzHRSIn+rV/REDACTED/DJrz7pne/REDACTED/++Lvee9Zp6app79Cj889rr//Cl7/REDACTED/zllMNWb7oJDoHUx4a+I/REDACTED/gxo3gKAUWAALavgYZRIOYdDrZ/REDACTED/REDACTED/REDACTED/REDACTED/9gGpryTHh3t7T/+0Tdf/qr/7JsxF90RPfIzjePUU0/++yX/REDACTED/REDACTED/dnTTv9vk14F/REDACTED/rnTz/REDACTED/REDACTED//feZ7v9HW1q0rqTms666/REDACTED/viKbncV0ftpT5Vvf/PxLj/REDACTED/REDACTED/lpUsXv/8Dbz3/REDACTED/REDACTED/ibDvKEqyorGHUMdGAKAyqPlGN1/REDACTED/REDACTED/REDACTED/REDACTED/zWtO+MqXv9/REDACTED/4Tj23QvAYH4zEzR/f2I48+plKhYfNjdHS4Xs/rGVkqbdOS+On2KkSBHhka2uxTQN/CKGqyfEk4hWXe6xA4jZWGMLCwf/REDACTED/Xr1XSbc/jh+996+29aW7uIizbdMnz//REDACTED//CHPy+OWxzsvdcu11//UDafx71Vs6177z0/REDACTED/hY48+p3UmVtCg187td9yZz09ks/REDACTED/HlFnaleER/emwb8aM1tak7G/REDACTED/+KFSvKldEoqnEPqESUZM1jGsa7Nrz//numTTk9YWpscx479t13z/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QzkJkr12+iPrQCALAhqRn0obR+/REDACTED/REDACTED/REDACTED/hLatWP6nL8+fPu/REDACTED/OKXv/rBD38yNjZm79fk/REDACTED/64t+krBr1czu+z7w4b///VJdLhQKF5z3oze/REDACTED/95771+4cMEB++93wgkv06q/Qr7Q2XFTe2ev3j4bo0Dj8djjT1x44c81N//REDACTED/t6mv+edxLj/3G17/S+JJHHll5zz1r8/REDACTED/JR0dHZ/REDACTED/REDACTED/REDACTED/Qq+O73fnD44YfpmQ+wxGvOWPF/v/+n7q5+ms+wverlsHz5rrpid9x199e/REDACTED/r/+tbqjk/ycS+MjZ57xrqOOOtS/5ze//b1uRVfXLPR4zFfGdl26M1Plox/5bntbF1FsJTWP+j//8+0l3m2f+9yndlsWs/REDACTED/ja17+57rnn/Pe8/T/REDACTED/REDACTED//skFX/zSVxGofOiD7//aV7+YkPR9/REDACTED/ZoPmxhURrlqwm/REDACTED/REDACTED/REDACTED/REDACTED/btUiauW5oM8h4s8ccSH/REDACTED/REDACTED/REDACTED/udd93zjf/REDACTED/REDACTED/O9uslvfOOp/m3vO/REDACTED/REDACTED//D4489lLDrPuLwQ0ql73a09eqalMaGv/zlbyfeoPH8wYceibrl3/3+j5f/44rHHnkggYE/8YkPvuqk0/REDACTED/lrh47LHH/REDACTED/REDACTED/REDACTED/REDACTED/upXv/2fr3/F356WLFlUreq39WJc+ep48YAD9km8+Sc/uaC/b5EhRpDcRNfk0suunDGje/REDACTED//PHPp5/+7kMPOdi/REDACTED/REDACTED/4lR//+Hz7z5+cd8GGjRt/++tf+Pccf/REDACTED/REDACTED/REDACTED/REDACTED/TJx19MpgwUQiCGYd/REDACTED/REDACTED/8f1NA1n7CychjNFn9nMhFg1Nqv5OL5411Nnwb/liM09bK8/REDACTED/7ovDCKRJyTe98HP/LJj3/REDACTED//+Vv9oV/REDACTED//8FVTz6VaM7Z7//QzFn9/REDACTED/REDACTED/GzZs1auGhBf1+/5GWcaKzezIeGBpBDtGthvGRMoBsByV//+vff/O4PouEH/REDACTED/REDACTED/A89sl1ty/REDACTED/REDACTED//REDACTED/llggCxb2bFi/REDACTED/REDACTED/REDACTED/rzWllbsWy1/KZfL/st1T4yObg0yeWmWvHGFSMxb3XXf/PZ37Dtvu+PO887/WSL0gL5neGSzMUVVmMaT9E/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/CG7r3Gpx/REDACTED/YXHOYCmZSAU/REDACTED/o3HjM6FJm6FqFMsAbO66oJMShSnXUN/REDACTED//0dszCz2FOjq7t2xeu9eee5x7zjcPP/REDACTED/REDACTED/ejBlzWyCg7iGHJKNAP/3Mszt2DPpXrrrq6t/REDACTED/vqn3yfsY/fae/l4sTWfb0V+Ro/j8PDAKae8+itf/REDACTED/a177xkSt/REDACTED/6BGC3o+HNNgHdre0WNMoIkkE2/cQCAkbgUYVsfiXVrh/REDACTED/f39fqsFt4tiwYeMPf/REDACTED/0dXR3ztjnss9C/REDACTED/25de//REDACTED/eo3iQl//Q03fOiD7/REDACTED/REDACTED/REDACTED/pFHkjrakPTF/REDACTED/7Jft3ocuzsdWsU/REDACTED/REDACTED/REDACTED//vO6b3/r64nbcKB1f2qV3fx58xK/REDACTED/Dc1te/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/79Kc+7t9z2KEHlSs/131brpZOOCG5EM47/REDACTED/ey5/REDACTED//7ueveuXLp4J77dHR0WEASg7enBbx7aab/REDACTED/REDACTED/G97RAt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/q0bG60U870R9EgM1Wd0mDi3T/REDACTED//stMrF4tDwYIvMZsZGhj/1qTM3bdys/REDACTED/Gn8PeNl/f2tmpyWxocfefRR6fwqp9eu7t6Wp5/REDACTED/qt/REDACTED/REDACTED/Pt0+0QB7aGQLGv8hazs+Xnz0scd9zY6+/REDACTED/REDACTED//DP/REDACTED/REDACTED/REDACTED/J7unvax0g7ksBHZQzwbMIHu7fa/REDACTED/REDACTED/REDACTED/U71BV0wVkNM5ht0CDanLeVisVmBXm/QBQM/REDACTED/REDACTED/KSnoH+xd4neK/REDACTED/x9vefOpO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//PqB/c/YpfE6rjxxpvb23tm4FyCKFJjxe2//MX3dm6qFPJtXe39mqtyzkgeYc5lx/REDACTED/REDACTED/FOooa5N+raEY8XiRYs2bixr/REDACTED/QYgTIQ0qkahpXn7fLGynVqLZ+DPqN/dfsccpLD7L1jwAuSj+MsB+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Nm3evHHDRr2L/REDACTED/REDACTED/REDACTED/VXi5Q+IapBgrm0hmk2pq9nrqDdQ/REDACTED/feyZbumfAM3HY/MS95D8QrbQ/XXAAAQAElEQVSGKFJEIewOK/0y75gSslSmfQPaG/REDACTED/zz33/GX/uPLZZ559fv364aHh449/6X9//jOpNbaUpq9v0Xnn/fS9Z5/p3/LKVxz7t7/d8LrX/REDACTED/F5L4XCCsThr3HbnRmXhj17/v+I+VTSmkV95VXXv388+t1i8ZL41/+8hc0do1XR+FrPC4mduy22/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/CqBpVg6gG2mJ0nDVQNh/REDACTED/REDACTED/DuN/REDACTED/REDACTED/tesxplxNbK78Asbw/REDACTED/REDACTED/REDACTED/fDP/X66+/cc3atan1TxxPPPFULt+v931a45CuM9E/uHaGhrYGYCbN9UgKzvR/REDACTED/O6628cHSuNlYYOP3R54yivXLX6k5/6nN/8/REDACTED/REDACTED/mNKune7i75+jGnv/t7/7wl7/+zadLuyzZJdF7YAI9DDwzBX/S/NjT69ZdedU1XV1d9k7NXz7z7L1KvM//REDACTED/RPn/REDACTED/AyGpvafQmh8aGdD8Me2/REDACTED/0z+/REDACTED/2nnnn2Wa3Jnwp9e+bZtbqrIxVakYGwwnC/REDACTED/REDACTED/lsgOTsTKLLIRgoOjK/KzkPH9p90v/REDACTED/REDACTED/REDACTED/TYZKjk//REDACTED/REDACTED//REDACTED/9qkRNvvClb/f2LNQ1efLJ5445+qhEp/1qr8tHhyUmrcDV19aae/REDACTED/REDACTED/REDACTED/t2DGoJ7/uFmBnQN4fqe6u2WOjY6ecfJJ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/TCWFZfdS0KX2cqmQYtc0asV/REDACTED/REDACTED/mkIQG2YEyYWt25JGtj/REDACTED/O51tXr34y8esH3v/eRFLZxKF//REDACTED/JJxQM/REDACTED/REDACTED/Ggp+cd0Hirgsu+HHiykW/REDACTED/IE+uXK4R5ILoKJ4/DDDqxUixFxWapcHvnP/REDACTED/REDACTED/qZ9vaWtq1zLitPd/REDACTED/REDACTED/REDACTED/o1uyjIiYMSITVncpyCZNWR/REDACTED/REDACTED/REDACTED/M6elHKCbN/REDACTED/281++6pUxVKl3zbPOOv2XF/1GRcnsH0t22eXss8/REDACTED//wp5NelWTx3/REDACTED/REDACTED/v6j+thTm8Vixf1zp7dm/REDACTED/REDACTED/REDACTED/rqj/REDACTED/REDACTED/REDACTED//REDACTED/HVeGVYjmZI/g+9nc21PPrYA9def0NrS6t/REDACTED/+u2jjih08cRR+56080PsRKPuR5jsp8zAqaw/M9rr0/kVzOGG5lsd+fsltZu44dYr73/REDACTED//1rd+lsu2ak74lJOPXLtOg+t1/g0PP/yIMObug5FyzhGAK2v3P/hI40fPOuvUn/zkD1of5Vn66MMYuwIoie6599mbb/kXgGp3fPWrX/7CF7/87LNrEm/Ts+tNb3z9G17/uo6OjvXrN/zmt3+t1YrQR6hFMyCQXQ847y+UYb1Q1F/h4goBp6tZf7D/REDACTED/4FNp/REDACTED/REDACTED/REDACTED/jdGgW60Tmw8jjvh9V0d/R0dveef/9PPf+7THXEeUb/hG1/7yj333r/++Y1aS6bR7OJdFs6dM9sPYbXL4l1L5ZYM5MU5/REDACTED/REDACTED/REDACTED/REDACTED/Qlfzof31y1szFPd2zNAe/8fmBxilx4/XXvP/9X9q6rVSvlQ8/REDACTED//REDACTED/REDACTED/mLtRBMEgazK9/REDACTED//HMTlhcz+/sT3haHHnLwG96YjB5/7rk/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/uo/wP/jEJ/REDACTED/REDACTED/zwAjy6WACgxNBKp+/REDACTED/bqKUQpqrk2WzLWhV1cpVq/bfb1//REDACTED/REDACTED/wKtwHrS2do4Vx887/6cf/cgHE3cuWrRwUZOXXHXVNU8//REDACTED/REDACTED/wIiuO2tnRdf/Kcf/REDACTED/REDACTED/7whz/39syTIiaI1yv16WeeS50qf//REDACTED/REDACTED/y9a9/REDACTED/REDACTED/UIKSswmwdAiXnIRZVYFyQw2wG/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/p4JYM9ObXFdpTefryW4ji4kX9XrKjBD/REDACTED/Wpr3/Lry76WRBMu/PXb1g/OLhd8w1mx83mP/zhj33/+9+ZLqgvjQ8Hw1uAYzbb05ZN297/gY+8/e1vm9ZLnnzyyeGRbeOVEmbMQOFvyUSBvt2/REDACTED/REDACTED/REDACTED/5VjGdo1g0UaA1D5kkbwFpe/zr9i+pcCyIE/a3EzC0CJ955MG//REDACTED/REDACTED/nC+z7w4Y9/7COTvqFcKY0Wt4OJb/SVr39r2bKliexrUzkee/REDACTED/REDACTED/REDACTED/w3H/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED//JN//NNftm3f/REDACTED/3r39/REDACTED/1+99edMoprxYTHvfce99b3/REDACTED/REDACTED/pm2oIlr3o8rDxSir4Z8/REDACTED/X3LpH3//62Yjct/REDACTED/REDACTED/luO/REDACTED/REDACTED/REDACTED/uPuy3cTUzuefOppLRbJa/pGNkRCCvaSRTUQ6KcUe/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/mzJdxPxcFPJ1izy/REDACTED/8KubuNb++1zvrvb7vvce9/REDACTED//vH5Rx19/Np1zzU+ol+ogdkee+0/BomR/GNwx6Bt0sy+BdlM7h//uPKkV7+uMfSxvuVXv/7tO951euP7q/REDACTED/7/REDACTED/uotb3uHLi+Yt7u32tW8ubtpXllvgf/REDACTED/ehbPAaa7UZ72v9Xa0ZTn1cb64/Oe/REDACTED/jiV6OGKGuaqzvrvR/4y1/REDACTED/REDACTED/REDACTED//REDACTED/fPvIo467/vobN27chIsx5cB0b/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/9fZcf/9N3aOFSGNvROq+rxJnFWs/vBYcF9F3F/REDACTED/REDACTED/XMSkuIEbMGcx6T4j/REDACTED/REDACTED/REDACTED/REDACTED/cJZTW3KN6ukX9mF/REDACTED/REDACTED/XlyzZZe+99lq6bOmc2bPXb1h/REDACTED/REDACTED/REDACTED/aZ9vaWl9ywAH77bfPwgULN23e/Oijjz744MOjY2P2/fPn79bft9h/REDACTED/8+yaZvNk3txd+/REDACTED/ST6LpeLq568E+rf8pKX7H/A/vstWrhoeHhIq8uuuOIqh6+8+mSMcOGA9rZufI/mhNdvWDk2tt2/R0/FJbsc0NGOdhlqeGhg3fNPJN4za/bS/REDACTED/ts47DpyqSuLa1Ze1/qmMIc1k/REDACTED/2JixKJ7kPTNnLunpngvMligWt2/cRCnZ+vv799l3r913223hwoUjIyP33n//vffeX9LSqLT3ZHKFBXP3zOaMk/DoyJYt255N/REDACTED/REDACTED/REDACTED/u3lu7U8pxCJRYDBtiGwBixoWAU4/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/AwLNiOseuux48d+6uWAM7O/REDACTED/qGtuY7dvXP/rYLWI6R0/REDACTED/Qrx0a3P/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/hBi6dJ999//mEKhdTrvcJki9Uaxzz6HT3x3f9+8/REDACTED/REDACTED/PmLZ/REDACTED/kgPZQ5gm0cKSh6+zq0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/rccO1EDr2yWZSHXWSxtAeeMumB/J9AAS+spCa/REDACTED/V0+/Vi6Nj4/5M3yffY/cuOHZHYMDiUf0/tvfP3/REDACTED/REDACTED/REDACTED/REDACTED/+8R+xPnHS6e//zf/0ze/+6j/8h//buu5jQb/66tt/8/f/REDACTED//4x/9keMQcjOHUmODt26//6t/+2//Lf/qH/8fnz3tQaXap/+bv/jfffvs3//E//d8nUOHyxzYSc01s6/z5y0+/ASnh036LrESoPuD0XZ1VdHaNy/zv/7v/6x//9A+//Pqnly9/up9ZZf/0p/8Ct17kB2r82//6v/0//9Mf/t//9IcTH4pvvv7h7/72f/j5l3/cb/T9pp2dZZjchWzKl09///f/0z/8w79rPHzub1qk/+bv/rftV3/6439xENmBY0/Mph/5N//m//CnP/7nhktfbu1/v54syOefmhDW/8Qo2iO+//2//vT8u3/68d/reXzwWfjy1Tc/REDACTED/TV52J3Qvjev/REDACTED/DFGnZ1y1flRXxtce0Od/REDACTED/K46bxkg2ppmT43vJXv/REDACTED/JtXgf8/nqoP3NOSo5Z34+ZoH+0IdPpcCT/iSk8Vtxtn/REDACTED/fPSirzZP2luZBfHPn57WM93j+iVz6en7//2+/+xan31DTkHkDWPR+SGZYEWz/9M5Bqq6hmhgQ+9lhscM/7t/+qrT8/tmC/G29+0Rlw79ZrB/REDACTED/W4QYbwQJqzR+XbX38x5r48X9t/REDACTED/ua77//660/fOOKD8tPjVdJeEHWlm0R/Y22bkPDLzz82rWdj2X/44W9h8Osrflh+oT1wxPd1+/XLz190On9qNOZ6/arJBo2r+PTpm+vTJ5/F7M5H45CxxSMNgWcSks/hv3Y8WR+EZujUPv+oS/Tp2999+zdfff3t6cGdsCE7Dm/w03bnTz//+PLy8/PTN99+8/uvvvmusaS7NZ2fg51SKHr58suvX/705def1+3l66+//+53f9NY9rxs+Rztzy9ug/fkEcP0c3Tan4hxnDV++fLzT3/8x19//ely/fTt199///REDACTED/nbEfv3lj7/8+uOXL39aLs/ffPXd97//REDACTED/fNbd0aMn8vW3P/zum79uvKH/REDACTED/zc+MivPv3+d7/REDACTED/EcCF0U7Xg5IUtXLLnJYR5/REDACTED/+qr79v/REDACTED/REDACTED/6Gx6DJUCbugkaGk6AZkvjypy//6Z/+9D/Tuz7voJvTuY7+PR0fPCd1vv1ddH/REDACTED/REDACTED/REDACTED/+r/REDACTED/H//F3Fs7ybKzSzeO7+Er8g1U/REDACTED/6QD2d16srPHvoxhaI9/REDACTED/REDACTED/QPEos77+QunluJs9s3U/KN7G/REDACTED/REDACTED/sCj/WhLgZLv/REDACTED/REDACTED/4w5/+50foTc4w2wHLnZ/Bh+0d7d7f88qbP/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/mb50zRNVyRZ4bYj/REDACTED/REDACTED/REDACTED/5xz/CTddCemiDFl/oCqo0WE/vF2gfQT/V9KH+z7RLlJtlisxvlMKvzHlgn/REDACTED/REDACTED/dk30JAn/syhoIUEBzyMsRWZx8S/fTsJG6qeT/REDACTED/REDACTED/bzVRM/REDACTED/WulkyExbseSPjFBB/REDACTED/REDACTED/VUKKp9hM3epEv/REDACTED/zT+q+1D24BVxXRTQukTNtQg8mzY/REDACTED/REDACTED/REDACTED/AJ1t8uSaDKvsJz/yDJS2pP/UQJBkazQ1KsEsmunYR/REDACTED/fd/nQ8PBZ94u+f03/REDACTED//Osvp/REDACTED//REDACTED/Jyx469zc5Opr5pL/D/REDACTED/j9Uek94N/0Rl0CU+/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/cVqsHaw6wi/REDACTED/VyW9RGrlmXyRENfH83r6/hsgBr9C8ctK/REDACTED/CUOr/REDACTED/REDACTED/REDACTED/REDACTED/7Fz7hx88A7mcU/REDACTED/p4PB/pzuzyzz7vyetJkTKKG/REDACTED/qdsDMI2kbTsYjDEuuG5LSNQXLTAnE/REDACTED/REDACTED/REDACTED/REDACTED/DULc3vGUts41ddV+fRa7I0F/vMqnVWzJJp/r/skW/3k9pql/REDACTED/REDACTED/REDACTED/Rn8QLWC4aJthqCaU86gdmJj4oTvoWRu/HUJOHw/R3B7s9OgPNLbRwHVb6qfzNp/3z7QvhLH3Wjjfo43IV56Q429oc/KNftifRd/kY/3OfjkbeurvXDzR7PaTrx/rx+PndnARYb3HOAbz9rj93uthmT/06z/n+gocTtcb//rL5/8M/+fa018h4rcnvjKGJ/VwT3llpwPnrlq1RkUDP/REDACTED/REDACTED/RNexYQcVh4cX04OInxED4f+BIW8u7+/aMBnPio099NZ/9zL45Hp1n6/PLw/jyQ/X/REDACTED/Q/n55z/P3q3K+PnN/Xqjp/REDACTED/REDACTED/M96/REDACTED/REDACTED/ASsuZm7sH0crldL1/af5ZPWuWYrdlPb2bJhu7K/REDACTED/CSyrby/REDACTED/REDACTED/REDACTED/REDACTED/zVUfD+MMFLipKzZwbyfBWG3w0Ef/f7/91l+aTxGpa/H/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/TRUE2CP9rAiqu5La/REDACTED/WofbieK9lPru/REDACTED/REDACTED/REDACTED/REDACTED/iMfvFKQqtd+Lod2JwWvPHR/REDACTED/REDACTED/RaHoxONYxiDzmpKWYHvpG+zcQ4G8//REDACTED/REDACTED/REDACTED/sxHPSpMHypq8GueAebz2//lJmxZSDst5LqKL7MR8fjRpnlFU/5djutHm3D/O1Ojg9Jzc3j0n+ruMMp/ZjG52/REDACTED/REDACTED/g+//L/eRGzHE5Vm/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Lrbb/2GGAxT/RkV5UH1+306kc+7UN/REDACTED/s5hLs9K0r68//WgYkr6yvFbI4QkMk/REDACTED/REDACTED/HU6O/REDACTED/REDACTED/REDACTED/REDACTED/i1J53YPDuZrIBc34FlWCJTk/UxRMhTUYdW413I9+y65mTL6/REDACTED/a52PTAJal20/REDACTED/REDACTED/REDACTED/REDACTED/f30+NrGuj88uPV+ZT5+sr98+6/dR0rSI8ZlF3/UHt04JIEXJ0LTe0dY+fPSeI6J8XNw/REDACTED//REDACTED//qd199dTFM/d22fkXmQYR9Ib/REDACTED/HD0z/vuzstPjO/5xfv+vqwp3L29/REDACTED/Pi5iI7jGi5bdAr+YHdmaA/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Kk9EDRnZL1vs6+2HeHeRn+/REDACTED/sdOuycy7YBKGnzOmgatu/naEzM2bZ+D24MIOXguXZcGO/REDACTED/REDACTED/oNY2WFUHGAUO+HS5tgZ/0v2R2R3P+0Oty2Z48WkQ3XJpB/REDACTED/REDACTED/AOxwnCxbBI5dbX8/P39zu/068EpAAnHaEE4bJBzkO+Q/4rjD//nm+fcv9z/REDACTED/e4f/REDACTED//BYD91uu/Jp2LQ58TN67ield7bMh/8bhc2KGdgMcd/REDACTED/mdd3gMB+2X4DFL3zQf+y1+Om/sb2R9/93Vd/REDACTED/pU/vV/83U1+/REDACTED/Rzi9jf820SWZh02XnjEvxnGhT7n9fu/Mr+3vK4V3S+z/REDACTED/Hb6f4SUDHeQjO8nTlC90P/rnNByOzpUvNQT0ynJt0fnsEeIFA8v/REDACTED/arjz2iHHC/SC6lT16nJwM+Oq0u/J53bigxaZu3BykeV4IAf+/fXX/REDACTED//J5rm8/r1L0yLP/Dmv/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/J38FRHuy6r1t692/REDACTED/j4Qc8yLs29cNLS3LSnnmAIz/REDACTED/REDACTED/9/jtEAN/REDACTED/REDACTED/8gPI+rDiw6MDqE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ubz/Q8HCH3resornlGPQ5s+gBMett/REDACTED/LHVmU4QVs/REDACTED/REDACTED/REDACTED/R/REDACTED/REDACTED/REDACTED/VO7zyaz4plVllh/REDACTED/0c5/REDACTED/VtwX2LgGmrFkejTF/REDACTED/REDACTED/REDACTED/5jeGzXzwJH5agm/REDACTED/REDACTED/REDACTED/7n+wY/LWs/REDACTED/KuPLf+6qP0fcZaTkcUCkw/REDACTED/REDACTED/R3swvlN7ENnOQP3m/tjRtM6vt2NHBzk5ZK7+r/REDACTED/0WrNp2n788W4EaVnX2Kdp/REDACTED/REDACTED/b/I57dvcLyQNk/REDACTED/REDACTED/HGIdzAJV+Z/ftL10eOAzwIP/lSnh1aP2RBeEb/REDACTED/79ds2CsNtJiO99sohrAK5dV8/REDACTED/REDACTED/REDACTED/REDACTED/ja9q2/REDACTED/9J3bq/f1nvSefd+/7IwHAvv3v/vv/4Ztvvv53/89/9+vPfzr8dl6Ss6c/P3//9fMPK8oYaN4/D8CpFJHAyAIdpU1GRmjq/G11DBQs7HffffPtN09mjP10u/+ux2g4ke5u/REDACTED/lBb/REDACTED/3fU9/PXpQ/Pz11+3+nZ949vgAQjn0pGfuetJOv/o5ANlbqzYvFnXtejwtfzX6dsdof8/0LNw05CnqWyDjx/REDACTED/REDACTED/REDACTED//REDACTED/HWH2rHlzf9YSxnqdn9HH/B/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/row29eOYZ5nNnu5rRj/REDACTED/3C+nzzmboqGzwxod+sf4qLfjtl9//sVZjgEtXZ9l/REDACTED/Z3UeUIkSqzmrrN55nlZesXg/cpnRZRdY+T7fj/lh/REDACTED/3se7Fr8/gtOY9Is94vv6sPeticWFLb79+3/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/mnu7n8nS6Qv7meKkPRjugJT7Lfl+BYru/REDACTED/REDACTED/AEd7/0BTuO0vs0/REDACTED/MfUIWdUs3/2tum6wFE8KFsmysQ0xGeuZzX0o9Wt/IXIfv9KiU/REDACTED/0K5ow/KA6/OaaNGuEPL08Rc4jI8DszkC1Gtu/7Yrh7NAb/REDACTED/REDACTED/Grfkf/bo9o389dVU5Zu+/9nAXUN/r5LCNr9O+VPiAth3ykb/TL2Tae9L8HOt68/n//w79/353Tp/REDACTED/904+sSk/REDACTED/REDACTED/REDACTED/REDACTED/1M/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/i1yP73snn/REDACTED/REDACTED/GqoERhh0LYk610dvPXTvUDh/REDACTED/KtxalnijPpZwSw3QOB/MA+2O2r/1UAe43/REDACTED/8cOUnvr6Nb2ws/REDACTED/REDACTED//PCdMTQNR/REDACTED/oYtpuROMqcz/REDACTED/REDACTED/St1m3JhZ4hlnQticxYc0i6Sa8d/REDACTED/+uzT1W+jI/2CaQej/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xpjHSu3bsZw7OO/rSZLa9rPajyWPdJ7gWPp1/984b76QHgn8zdfPEqvWz3W/M59ByNMFdR9H4h/REDACTED/REDACTED/cnP39cLcoyP5K4w45Mp1YcI/REDACTED/REDACTED/REDACTED/REDACTED/PwH/REDACTED/Y+uVFKsxq9gD2nmh/REDACTED/REDACTED/REDACTED/REDACTED/vh8bNjZHxkbN13oy6HRNtPHt/Tq57o0iD6+7d8t7rvXdd+JqsLHPcfr6/M+u8hdtz2Pr3zAd2sOi/ue0M5h8qP3a87/6+ut2/fzly8MNfvBQqwD/Y438zwTc1a27qERESR81JS1F01kTW0OlIz/REDACTED/REDACTED/h5cHm9C3a73ruT3MfPNIZEo376UH/NNj0zY5eUNCEoCwUjGf0cxaq/d+B/fwQ+Bo6XI3lPOJJTyQsuR/REDACTED/REDACTED/REDACTED/3m8xJE/REDACTED/REDACTED/i8GHO8+r/a6moFbpIiX/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/na/REDACTED/nLd//8Nf/REDACTED/+Ph7OGn7Tfffvt1988WfTGdau/REDACTED/REDACTED/47E39rsMZ2o1TTs6c7/REDACTED/REDACTED/REDACTED/REDACTED/WPFh7EOMDuL27Te+m1zRRfH/REDACTED/QLtiom4HGx7A0LtZ88P7f/PVnErpWPtSEWzU+sTslIZHC/REDACTED/REDACTED/REDACTED/ug4THlMA3agBOAJrka/REDACTED/onTwlQ4YdtlKh6Sn/Tgywo/REDACTED/REDACTED/REDACTED/lwRfTTa+uLR+vHN9b+/REDACTED/iP/9GhMPUb23A6Y1+LT8/REDACTED/REDACTED/REDACTED/XRV95/O64BdM6mUJC9zvt/REDACTED/RyxcIK2A4S7/IedVLAoHcY30rw5k9pV8/fz7l/REDACTED/REDACTED/LDSZAy5hAcUUe2orl/REDACTED/REDACTED/REDACTED/hdq2yu4llkP4Wqy5ltE9/REDACTED/sTjN9/UjR8ODFJ1faE5tOdLz/eM306fjMk/6+oGdje/ScD+7XK1fnVc7bv8nFaFDRZDX6C7X/REDACTED/7lp8/8Y9/+BFe/REDACTED/REDACTED/6H90fxohBl6jv58LtKN/REDACTED/hwZJ64/REDACTED/PqPfzedai5X7bxdu/Bqm5J9yV9duHUav3wv8O3njap73vP/xw5hgMearhtO84vw/Wau6v27IiL8WOcZU8k8c+oupL6nXeLbj/EjhvzubB+STgTJw67DOrN/REDACTED/S0NGUI7LzWU2fc4aAArf7/voCCe9+MN7ux91rwk/REDACTED/REDACTED/KhOb/5Wnu6yR5NQAAEABJREFUwEj/REDACTED/REDACTED/Nj9bZU2k4d7tDj/gSpYDmTxPps2SEHq7apXi7X6/REDACTED/bRZDnGekKvP3w/REDACTED/REDACTED/TzGdrx/6k8MWBcY/E5JzzloHfxzcgBebb/xebwYO6g7u/KrbtKvXd/eCnl7bFM7VnC0wd9NMH/W/t23f/v1px/REDACTED/REDACTED/3O0AS34vM52XXHm/REDACTED/k04mkFZk+oy/REDACTED/REDACTED/VkZims+eDLeXTOYx782Jokop/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/b6B/REDACTED/REDACTED/DBDYMWcy/REDACTED/qv/F/Z7+xLF//haHVR7tV69dGBucY2K0+HCaBuodfw2oT/REDACTED/4nyFldXP2liFED569LiL/REDACTED/REDACTED/+SQnPr3JBlhjSM4BG/REDACTED/REDACTED/P1+/REDACTED/SnifJm0SJC3XLuMo3tqNk2ZJhLCVLJ+/quBoVVxdzmIZPrZjAY3bS1Sq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/7+/REDACTED/bfnVs0z9LG4dT5IEnsciX208L/4p68aZBsuAHy0/iaRNxla7kl8EQ9CMEQDRc0zTCf/jpxSb9ZAjSY/REDACTED/REDACTED/+bV6OtABH/Bmjnfq5t9/REDACTED/REDACTED/REDACTED/4kDI+E62kag1WXnXx/KDhwHwc8/xv8CFyXAUXR4KrdYCiTlL8PlnXl/V+6+iNhgUYI/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/MOFpx+/t3/sS/SnuxO/b+W19v068aVzJZ2Bfnh/9PPZeObJn838jSs+h7Z/REDACTED/REDACTED/WnS1Uk8/V6/zQPkx3CnE/REDACTED/REDACTED/xsBYRp0i2tB/REDACTED/REDACTED/7+C+ZfDgpIFumvP5s/qNWXoXLk+Xp6sV3rCKIZIAzZ/REDACTED/REDACTED/REDACTED/4T/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/c9oks8/u2c2JFWdn57RoihMaU3rq9/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/gyOG1bWFGTmmo8mD7WVnvs/REDACTED/REDACTED/1vjjJsBLt7Mvmd2GM0YUHm/faU/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/qaXiQb8zmjMJeWxl+q39v/16ZDUeXHf7+8/4Gav38+f/YumvLDrFI4EraJENS/wMehuMocOJgS5UeIBibX/+Un/REDACTED/REDACTED/9/IfvpZP3ynt/y5NlMnx2ePDQ01oxJ9fuuX9/f4n+mvrD8un3l/REDACTED/REDACTED/REDACTED/IamTWLZVlrrf153lP/8Kf475kHumt65/REDACTED/mrH4ftc13cxZt/24kU/REDACTED/blmHF2n+ridPN4orqTGb/REDACTED/REDACTED/cdMcUj3B+UR/a/REDACTED/REDACTED/tCFiz2so8uUdKyFM9nA1t4zvc/REDACTED/mCH9z/oK+TykFPfeuSaHfaPkWvO4Hw/REDACTED/bBaZvXqvuPtbReXfPLYBEANQPl2//REDACTED/59vLD919X/na7fxKL0+95O/REDACTED/3wM6P8Dpj/REDACTED/REDACTED/U8Pul8Ity1aU2q4eVdVAfPalPNG0tT6/REDACTED/REDACTED/REDACTED/REDACTED/8dab30bYjj79X/X9b1U/REDACTED/REDACTED/REDACTED/LvDLgn1XNPkWX67t/REDACTED/UFW49SQIKEXm0+y9Vs3UVFyHV7KS+Ky3kBPfQkVyZ/6bOXhSx+tk3qWTM/REDACTED/CgzaT/rTpzZEm6FXFvMKYz0GAEK7J8/SdOhtNzdPSmzZrNW4jYWF5/REDACTED/gWWZIBzhEKLE8YQ5zABzRTehFiECqu/REDACTED/REDACTED/+Z/7wg8lN/REDACTED/oP/VBX3QnmDvHe3M6mnyqOevP/REDACTED/pN3RZ/REDACTED/REDACTED/REDACTED/REDACTED/hYv7/bFUP0Vcc6GSoJsc6n2K/vQI0VoxpMO5xGDJ8Wr/REDACTED/REDACTED/REDACTED/REDACTED/PIj5cG9n26mPTqFrEN7+sjh+lZ/REDACTED/REDACTED/REDACTED/LApu/REDACTED/qMGjnFNCo8/REDACTED/Q60NloF8nye/h9eEI01w4ucG8ox0DyW3m4V/AO7Zpbsuuf0bPx7E+7LdRHa/0F7++vo6PxyyHcT56C7/vNL1xJf6obvit6+tTXdeXz1/REDACTED/MkW1pRxrIiMjdrw6LRJSiM03SL8vN6/REDACTED/REDACTED/1k+cu+6/Of3D4e7ey0/REDACTED/REDACTED/tvWlyVoJXfHAmwO/REDACTED/REDACTED/REDACTED/REDACTED/2cAnEcim23Z/oNzMVvya7g/V/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/egPbktPW67faC3d9d3rAJYgM4Af/T64cnzt1//REDACTED/vqH5+++//REDACTED/1RcVid3Bz/PHKoop1+fl+g2Vb4i/REDACTED/pDDPROX8r/REDACTED/REDACTED/REDACTED/U+ZfCI2LpKfRdPrmI/REDACTED/bjOZ3weY2rxmHkn02c3E/REDACTED/RMVgy/t71Xrli30LsqYrn2t33HNtDtTc6H38EA7niHzEm/wHgQJ1q1fGuKouYW1Jq8OBEV/1addfWfL1TxSVWCwqr/REDACTED/REDACTED/REDACTED/ji7ZM/UMaldFOyPxxexCCMzrCb11zQPpw/REDACTED/REDACTED/qiN9ieaMFVqr/REDACTED/yWfvkm0/Sfu1T/r4kr/REDACTED/REDACTED/REDACTED/0Pc4ehw3GniVaOs9RR1Bl0Xr/REDACTED/REDACTED/REDACTED/ZPrq6bufEvy/REDACTED/REDACTED/PZkJCloW8qE0/REDACTED/REDACTED/REDACTED/4yfvT/REDACTED/7xjEOSV5Vz/zG27DwRe92X7VBeGVNri53E7k8s/p/5e8Nsz96+d/REDACTED/yTz+tmiui/REDACTED/REDACTED/REDACTED/REDACTED/J44Xa+T/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nM1r3Thns1n25DpkKXnHPn54Lx7/nrtqa8/g9v6Tc4QBHs/Oo37+gB7g3dfXJ/n1V7+/REDACTED/rC6Nlv2POF5SaoYudMlWovt5eG65/B/REDACTED/7oZV3q+/REDACTED/SD/W85bnv4UD7/4XTD4K/REDACTED/a/REDACTED/9VmF1W3oKLSOlumcOGw5yyi8SbPW/REDACTED/9MfP/9/REDACTED/NyMSHT00FbWjMrU1s0xy+8jp/YEmqoqVal1/bSK4VyTS3BfFNaq29Sm2gz/REDACTED/aYyvdVengnl9OJxv21UACi/4FOOrUYfvFVC/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/rOaOPz8r0xd/REDACTED/REDACTED/REDACTED/REDACTED/HGdSHSgzoWzMNA1vwKTTC0dJQx8cdMS/REDACTED/G42twOpO3RCaLFq/REDACTED/REDACTED/bFpZ9T6ixUb/NZm97ZDoGC53bf29Bg8h7/nFwL9Xp2Pd/Xw6uESrfMAk9/REDACTED/EEn4Od4OpWDlgAo5+m/k54Ool8tZ87h8VDdXACh2+08/P/Yu00tvNx/REDACTED/REDACTED/NiDJzPyQiVRAjajQn9YMak7/KUA5l3Zqk3tFDpyo+/lUMPH+8kfvhtmfudfWi8fV1o5WXVnM/LvZH/REDACTED/REDACTED/REDACTED/TufQF2+313L/REDACTED/REDACTED/TM5iPddKB0xDZ8Z/REDACTED/REDACTED/EIUDQrvqEWy5p9QuH/REDACTED/REDACTED/REDACTED/Qs/FY2bCW8qyQA+UMlCy/SPj/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/7/fe/REDACTED/REDACTED/DhMrTXdwlTnnQ3/8i333p+HXMsffrXxYOti5Ls/REDACTED/REDACTED/FLs4DjGRS6w1/cBgWzoG7jdHI/REDACTED/REDACTED/fJUmHq6/9XNC30/o/REDACTED/0bO55st/REDACTED/FPEeS1wEVYnMfP2X+HppGJzM4U/oQjxdbHcTiagVtQoZoZ/sG2lGm2LyYY6zkuT/REDACTED/b/REDACTED/gWKFI22fLv494/QuWjVKE2S1hViw/REDACTED/abjv9ys989cOvXmluv/REDACTED/t9r7oQY7xo/bkYDZVk94v/REDACTED/i5FTzIVB8yE1NKihQidWhmF/REDACTED/REDACTED/SkdWjoZLk/REDACTED/REDACTED/j2lzvj+2en4OZwwyPR9v94DM9Py08+PMlDYdL/x4af80pmXdytU2C/aTRx8+Rq74OlNG7o/REDACTED/REDACTED/9Fe8/BKh+s7qPNE0x/REDACTED/REDACTED/7Pce5MrI2iR/REDACTED/REDACTED/286DjQX0e3e8Y9ohGiT7W/REDACTED/REDACTED/v7ULv62fXbO2J5SMvUR62yJnPTJCSPx/rL/z0y+d/REDACTED/cHC9BNw0U//uHpvv1q32MWEmyjwZbngW6T/REDACTED/ZJJ4//7a+1m8CpsJk2EzG/T1FYt/44vlw9v0cIIt+jv4ocVsizCT65/REDACTED/REDACTED/h4nHF2Oi7t/REDACTED/2jCR9UUwCud2/REDACTED/o+CP6PvED7+If3L1bwxk2S/REDACTED/tmOZ/F7JVbeL/REDACTED/REDACTED/REDACTED/uXujIxve/REDACTED/wOzwjIecd6PNg+Z4+zFJ9eZ3B1veaP/AOFv9e/XnJzBPdy/REDACTED/R2Xr6lxXZr/REDACTED/REDACTED/36zs/HOzpAfrkBJtJGmk/REDACTED//12WcsBfufx7XF+IAsmaNnoADOI+/jLxYPfLHs0EvjGDZpAjC/REDACTED/REDACTED//vzvPwTOfb7vo+OB0w5C74P75/REDACTED/JiMaeiKSJhEH6yhM/REDACTED/REDACTED/REDACTED/wqCUz5mvabW4EQyyNmclWpj5oDzT/7/REDACTED/REDACTED/x5DbEP/nRHyPmUGJ2sU/REDACTED/REDACTED/REDACTED/5yXl+s13jz/fd38HSmfoYO8tYr7QOu36e7kn9/REDACTED/REDACTED/M0rJZyYNoTGH/GvUFLP9DuPC54ekdZeJP0tNBZNJpbE/REDACTED/rb9Xb/5cv9p3ds12/REDACTED/REDACTED/REDACTED/0Ly+/QfgK/REDACTED/DGeA/dxqoEuxltlqNoU/REDACTED/Qe7qeC8mO58B9d8lvd6VX28drFt5+4/REDACTED/H+Y7rK/REDACTED/wEBXF6TfhvhT6vaNzJz1R/REDACTED/lQ1V9ZVVX3JXfYMBgqdqDaEUr+/REDACTED/REDACTED/REDACTED/TgefrbJvs0Vlk0I7Rmw2o6/PVO9/REDACTED/ytJi7MQQYnaI5dpNcwHad8LG/V2h3Imba2tdQ5Gwv3vqc/mTajB3GOEb/REDACTED/REDACTED/5/xH3JlqOJLmWGGBORmRWVm+zSDo6R0f//zfSN4ykeVqeXm9VmUHSDTLcC9jiJCMjq/REDACTED/s0JNlfzJSxMWeSJlBgDi9861WY/REDACTED/REDACTED/REDACTED/Wgfgu6KavPdtPOEfuup0fXrnaMmzq07H/vSV5tUe/XCqXwaJyov7wZuUGotaOLgpfXZcvTvC37/qxC7dP7/Xj+ukKuoKpvjW+mm+/op6yOOI2xOYsGkFfn9uXs8/REDACTED/n3/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/JXbi/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0tByrN0+W0VUeq3N5udo0KPZAQa/6WBDVUV7E7nEOD4FQH/Z4/REDACTED/QmW9d6g/REDACTED/3RNbtry6sPV/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/7um1nT/REDACTED/05kXHVfJ/REDACTED/REDACTED/LjeYHSV0qSnJh+eX18cOrjJqzc3/N6ulx0YH0IbudC22Uy/REDACTED/REDACTED/REDACTED/3NVr57keyi2jfm3cYtF6eL/1K9h5eWwhf1Y/XQ9POyjqH7Tth66TIPGPPOaffj0KOT90/REDACTED/527+azW9KlUXyKX4oamOP/qLN7OBzb3m/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Pr7r5ybpuxfTmjD/OlU709msdpplgmJZnGp9phUU8k4/DbHpZ6d5XhDPzOdUBt9WF9fKes9/wQ3hobGobTu8/REDACTED/REDACTED/MnjX/uCofuc681r/yCk/REDACTED/REDACTED/REDACTED/OZ2Yo9YS+8vBmC6wvmpjXkR/r/REDACTED/g9u0MBgxdUU0/p/2EJMIdSRlJXW88ak0Azbv/REDACTED/fyfLU4W++FkDuE5/mKjRfq/REDACTED/fniV6eC5+xT5kc8Hn/8by/ruW99pQT/Yuv7ykLm0C8nPhLGHR+yT+tHiu1HQp/REDACTED/nu9TmH9t/99/99u/7Lf/0/9T1R+bs83g93q11//+V/REDACTED/3edv+4yy65n8EbHBcDd/M2zcl5l/AyJE4EgOfywUmn/REDACTED/REDACTED/REDACTED/3A66GDy+CQ0NxvG866fr/REDACTED/WK1/qTVwsw/9Eo07Ybd4apN8xXYSgrMAdu1/3b6dt//QFC9aEz9/REDACTED/FfXndRHtGA93+y8mkUbo9srXtjFy/NIQS/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0/REDACTED///xf/49/CY148Fv9anI/REDACTED/msdC7PgaGT/REDACTED/REDACTED/REDACTED/REDACTED/dI6LDnmcjhULcZmAn4eC2Be/0lvpT941MvTT3ZuPEl1/on21TybPMnRq/QVP3qSfALpCQK/jJo/TcJEEYtYNp1GSS/REDACTED/FH1FZuAYp/VaZd6xmKPJFjSdJi5xbAca/REDACTED/u9+yWQgjbEYhKZOC7oF+XB/REDACTED/inN3q6wDUwCTeGasKvDP/REDACTED/REDACTED/gfLQ6qeyqss8KPl+3d9rP6//G//BTO6P7r/YTvtYLEc5dky8G6Zv/REDACTED/kj3Vv/1Sy/REDACTED/ZU574e2cps/TaZuT4VndP70LXc6cBUn9vo5g7qXZ/f/REDACTED/REDACTED/REDACTED/REDACTED/J3PaPb/B/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Wa+8SkfskWaNR/REDACTED/REDACTED//utP2pjvFXS/REDACTED/REDACTED/55WgtR2Dbq0PPh+dmde+9iS+x9r1/ZpZ8eH5D0W8ZwWKIakTOMgd/dnvfXdVx6lO3q2iO/7eF+fir35Tg31l+QRouO3H/REDACTED/REF3HYygzdPzD8dWhqHXGwvGK2v+yADEY/xOyCYP8TxtIqBPz/REDACTED/iHzXPwZJcfT5jl/REDACTED/REDACTED/REDACTED/REDACTED/sViX5CuN0StVfSews2pw3L/REDACTED/REDACTED/hCHCSVhpmA7cLR5PSsSwE23/REDACTED/K4krDWHq6VNV6erbhQNfzpP/zp6y9f36BuehgD/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/XjrioQnZ+Jy/REDACTED/urxdYG01ZGNi/REDACTED/b8zEzs3m+oOWOYdkE0YQx8x/REDACTED/REDACTED/REDACTED/b78r94JnKOrTmo/zO/Xfl33rVrnB/WtauJ/6hst6Vv3dUBG8wcV8Tm/REDACTED/T/0j6/FgsHK27flRPg1QfH799m/NeFoj1rdjX1WSs/gvSGmMq4x66Ss0eGTRP/REDACTED/REDACTED/REDACTED/zA9+Zocm+e148s67kPJEWOJ/XjORoOHGt9bCHJZWX9XQvFsUN7bP56Ws/REDACTED/REDACTED/mztCovHJ/KPnO/REDACTED/QApqW/REDACTED/REDACTED/MM9R+x+XL1EoGqKcCp66rY/W7S3Ohwyw8Yi3oV3inET/REDACTED/REDACTED/REDACTED/zupflbWZB57OY/REDACTED/REDACTED//h1JaDfEVR+7KrH0/REDACTED/VYL/Rz4/uCoeDu56zx9+/REDACTED//REDACTED/r6Q+iP5t8lhIK8gNBGnyurnGz3/1Yspi828Tu75B1dfV/NO/vA6Yzu2+9PbZkc/REDACTED/KD6IB8G9lMplifsllkwKyamHGcL/REDACTED/REDACTED/REDACTED/REDACTED/3Lg6F/hymRd8/Zh8Trux8N22PYfwHMy7S2fGeCJ/kpCXfosHE6Lw/7oUNDN4trM+ACEtmDTZv45nl/REDACTED/REDACTED/REDACTED/eIhNW739p2zx96gMMZU3Znv1/REDACTED/kGVQirYgPyO4u1jAPu++3bGG/8JW+kTlTUh0ZXhHCV4Q/REDACTED/REDACTED/rdA+Dsiw+MWsy/xfTGORNZJ5GjQdq3Gy5Jmof/xxc/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/zQaFr2RjsYLpQzamm0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/NSO2I1ICJLS4BImaZ1jgEidage/REDACTED/REDACTED/2/9haCUaIIuNGZ2K608JzHg/REDACTED/GyDXbojgTqfETkaJg/REDACTED/+D79/u7z95S9/ltnVp68Bk6lsz8qDl5553WflfrV/7yvZiNHf32jh/9H3BiPz8TLG0HI/WrZT5Vgei/px+ZMnMtVff/367e3PNXD9K/1roGk10UBYDh4xcnWGV46sWgGP583UPn/REDACTED/c9n2Z6J/REDACTED/f/O5/REDACTED/EIjDGTuZGg/n2nxY0qe/REDACTED/u/86ff288OPxU/REDACTED/REDACTED/REDACTED/n4bd4+zpxh+iL45woJxR/K4hnGEbWB3iHIy/REDACTED/REDACTED/REDACTED/REDACTED/i886Plpkz7D//xP339+vWvf/1bLoJ5yntZpiXy/XL8qdNAqtwNrT4d5g9d4xxbr0MG0UdccW/eYfTYhn9m/REDACTED/1/+p/+59/9/OV/+V/+108vfwD13ekCbdL1gTiT/YH9T8s/REDACTED/REDACTED/F/REDACTED/ThdtWp3iayMbf0+3L81Dv8X+/REDACTED/p8YYcNnb93nsP9cmrZ6P10HFr7N/REDACTED/8fzk6ZNEI8S/c0R1gfj3AOo5/REDACTED/REDACTED/KVrqR/s++pr4Bj2fP7a2BA9fxzyFJ+P/oIxBPC0nT/2Ra0XhNicVnkbt4KMfdWnN+u/REDACTED/+rqqN987xYg/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/6r9qkMg/9hV+wHXj8Wn1/cfFxOh47HfKX/79df/8l/+N/xkjPncmby+0/REDACTED/REDACTED/+5f/6l3/REDACTED/2ezlbmaI+RMDLroeOk22Z6/GD66qCrMgQAue/M4+vUs6mH40ll9F/REDACTED/REDACTED/+BLfVzF0ynurX+7v51ucrxelzkT59zVx/REDACTED/REDACTED/REDACTED/+8hjYxVHjBsaO/REDACTED/LTHQg+LgkUxhpHzC9O5oX9/POlhhyZfP/REDACTED/UM882I35BvT8jnAn/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/2u/MaryFiJ75aH6P60PDlbjvJ0z99/REDACTED//3+9i9r6ketvWzt//fO/REDACTED/u3P7cwKFkTG+Ld/REDACTED/REDACTED/4samsD0SC/Cuq9NnTdLYcPqOrOg3xj14/ukmGdi08/REDACTED/HX+aVoWiiMiEwTkW/REDACTED/5rc/+jJ3yRvc9tMpm/mHSTLLzBSNjkMz01/REDACTED/REDACTED/6r/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//4Gx9XJaP8iSMPS7zfrubqaw/REDACTED/IdIFWbFkRD19Qw1PJPnjH/REDACTED/O6Ht+rxQ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xi/t2PNWLWav/REDACTED/REDACTED/REDACTED/IxRmvF/Oh3NQH8/po/REDACTED/P3U29xmCKth09IhrPEKtCu/t5lSJV65MznQDYNZTq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/h9t7Blkh49qZofka8/REDACTED/REDACTED/HmZnvjBj43296q5fTp1N1NHx/REDACTED/REDACTED/REDACTED/LY9GGXuVq6kLRZLx9lgW6BY9ISi0h/YKY8QzUaOdA6UqqEHR/JU1/spw2hqDft1jww/PxnmhEvkwWrmZbxTK/Tviu/REDACTED/d40/qYeQr0eHvvgc2Dze9r3JDefvjPpgfY0//REDACTED/BcZx8vflx6C8DZmO3GqTZmqQ/REDACTED/JRcq17luOU40lH4aiMbR90vkJ75vEh/jY5+jgo5IHmfXXDSou01k6/REDACTED/5YtImx6y6wXp7u2CpFMA8n/REDACTED/REDACTED/REDACTED/FcmOy3/AgF8iMTRivAOWmrZ6bGKE+NJMjK/REDACTED/FKjS/REDACTED/w/UzlQ/1tpbB206otjrd/7hMPVMX6e1D5cGmfaic+ps8/yXt4iad+f2nl+WOnfxemW22uzb/REDACTED/ijFIpnvkD/8te/mHzbLycpU9AbrbhlL/REDACTED/REDACTED/uS+/REDACTED/REDACTED/REDACTED/REDACTED//Jcntmip/v0YfHZ/cvHTD524+Nf58Dp3YbBs9XdGC/S/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ZOshoL98hVi3lknfWpIPrc/REDACTED/REDACTED/xuuOnEgHyo/VJTIExesrD844AnJzbJpp61931L5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/VLkTPEtkoy/REDACTED/+wgSdpRKZ7RmUUD7s/REDACTED/REDACTED/w2Ac8VcyZnAD1zNN2sd73dCJGl2/nFkZkc5/REDACTED/REDACTED/REDACTED/RSgZSCEWsQ/REDACTED/tjuPSzuSl4FSCJfX6Xh71eE4ZJ0J/TgxMnoMDbTmdsWoiPId/REDACTED/817OrPHlEfz3/REDACTED/GoM6/REDACTED/+bbCOHZtpj/REDACTED/PKSQoBvq/h/REDACTED/REDACTED/REDACTED/WYOEF+ZMiUEv0jerqMq0/9a28Q8/REDACTED/REDACTED/PnchsOe8p94AoFR4rfcfh1rEr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/oU41cwcZ8McAYKyH/AfgJIN6CyGKfdp/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/OQ/i6Rwa9YOBn4T8PPH0jquU+WjuJ/Ik1S3Cno1j8YP13y//REDACTED/9kfJjH2vt9jf291l9TpgO19P/BvXaHT/u63XWQHex1pJFW49wG64a/Sq//PpvTfuctt/REDACTED/+s9OW2+2rJQOZPEI72L6p/REDACTED/REDACTED/REDACTED/GGab6sv37j/UP7u/C/PH56RVjevfhq7O3B/REDACTED/nU/Wsv3B7diOKeEAn7H/7PlZ8p9sP5+sw/qrLGnv/REDACTED/REDACTED/fdLnuzQ6UFGGuy9rZaj9ILoAh7e/REDACTED/I8tWHptelcVgHKE/REDACTED//REDACTED/REDACTED//Kn59bPPe0/REDACTED//oR++4JH3MPU2t/REDACTED/PGPf2i05fb2xfo4mud/d93/REDACTED/pPhslpUriIZczwg/pIM3qsn6w607yse2S0c9050y/fLfP3m7ycmkamevTvqV33ssHRVHXYfKKDmk/REDACTED/rXqYCHC0LLLmMR34/ntDnm+nHuT/REDACTED/REDACTED/REDACTED/aSfPpsv/hcnmJdRwLW/REDACTED/REDACTED/+ASxVCSaMzXWzI/REDACTED/REDACTED/glpyBJmWoJ/REDACTED/REDACTED/REDACTED/SDEs/REDACTED/nHTGV7elnkiC17sxdkmqPE41DEe72kAiS/REDACTED/LhugE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/71X//v47ed1PX/REDACTED/o6PXMSGJJzvq+XmSWTkCryz+RJSWXMJlYmy/REDACTED/eFD95vKQFL9bLvZR4XO9PhxI+/REDACTED/fU4NW7LDTtlDgayVtje//REDACTED/REDACTED/REDACTED/rGPfugh8U5Z/9Fs20T51x9lI/REDACTED/XDu+Mk6ifR/EP1Ny5m/q2EostHRJN/62lRsfyIXxZ3j+en6+I/REDACTED/MGUwKlH6RaeVmG4oFpi7dKYVGamBKedpYddPX/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/a3ZcdD30wHtkIZnYN/REDACTED/0/nUmIwLxN1/HCD299uXyYOl8/REDACTED/REDACTED/REDACTED/REDACTED/XBPWVpzd0zoyG6tvjpe/REDACTED/REDACTED/vsumesU05hnW4M0RsXh17x59Qln2UmCnz/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/kc731ncOUFsFrkkxYJSzWAIMSTa/REDACTED/+GDx/REDACTED/nWbsIAc8Q9pBp5a+eMI7/REDACTED/REDACTED/REDACTED/h19JbqqCpBdOtTdACpGvSCZkXehFxvbLh/REDACTED/puPPCzeqLH30/aEB/67/BO60to3soys74av+/32PRF/H4MSoyYzj9ey/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Wt/REDACTED/KhQKafIwt0FVpT9G2/REDACTED/REDACTED/REDACTED/mKwROC+yFfuX99UFU7XSkzFe2YX+3/atAVSdt38Pyk8fcnzs/dH3nmT/Kh/9o/T/REDACTED/dQUWY7VrE6mufOS9o+Xf/REDACTED/REDACTED/9vWO+Y/8XesnzoIYXdClkdz/WTjfZdYSC/rxzf23D/2WZdR0KdjIu/e9ugeefbr5aY+yQ9+b49/8KRN636fWN2p7BBpSIBp5SSwYlXNdEc6GtR/REDACTED/REDACTED/JDfadX86vi71p68/pdqtyxI0vj/REDACTED/REDACTED/REDACTED/REDACTED/NqQEZ4I+JYCzw3MBBiwM+8EOBD8QCNVEEo/REDACTED/REDACTED/vB4/evfn0yNZP3b9dxGVn/REDACTED/A+ugA+/C+388tN/uHnQirs4CQD9jRokHB4Q3iIpESSErrttukp/ViM+7Xxumtp27l7e/CT60x+/REDACTED/Xq+9e2GfEXmHCmqfdH16TwzIqO/jPlHoR7/REDACTED//REDACTED/C2+ii1p8actbxly7/zn1B4IwG173m4v+/7p1mTgJgBftd8Yu+nJXNhYgvdiHS/REDACTED/GoKWyhXWrxZX/t+yYeq6OAMO/mP/qbOIRkyvLcDoOdQcuDuF6NMI/REDACTED/v4k2Skt2lW3e8tDCW6iQDC9dagX/BNtW1P1/REDACTED/d2pG49X29ft2//5zijH56PZJcL/REDACTED/REDACTED/REDACTED/CBfu4g7NtYNyDRYjjDcYDahRon3u37u7cfrENFEYlYLY/REDACTED/onUX/yzvpJ7Bgr3g7+Kq3QWgn1M6upX1agtn2v/REDACTED/REDACTED/REDACTED/tQNf309W1/REDACTED/jUge+fJGTO0rs/REDACTED/bfv1MhaMU+PhIDShhDrT8RW/REDACTED/Ved8Te/NL7VvoAe/JTD2uHmUcl3drZNI7iHTulpOlGM9/q193bK+jlS/mqYqUri+/REDACTED/REDACTED/CfReAfnY3jbrWu15vsLtanIxk/GwtFOieEzR9zy/REDACTED/REDACTED/QjdqNCXxv1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bGIsP64/REDACTED/TRMMpwNzWOVyy8YQr7RhhttHXE/REDACTED/REDACTED/REDACTED/mj5N7Tzrmx35YmT+uvf//REDACTED/avVjd392rE9xQ8RYWzdNPbbW+y/REDACTED/REDACTED/REDACTED/REDACTED/vMvu6vXu/REDACTED/REDACTED/1ddl4mrxPp58L3StOjh1/FvZeufn/REDACTED/wPD607R/REDACTED/u3pCXFj/REDACTED/nA3VzCZFAq2X2/REDACTED/MEXfWgLtmWebEe0ZaG0Kp/REDACTED/tLxpnHSTFRZQ/REDACTED/e19/aNyUnQ6KQV1l2M7e/1g/REDACTED/1U2mzcPU/vVL8MZ18/d27Yq5Jirh8PngWDj5T/KdcHzOjx+si9fGZAD099ff3DaXsF/REDACTED/Jyub59ffvy+dPrp097/VJv55wi34fltG/REDACTED/kvVnP/bReap0ac/REDACTED/Cvz9H1lfjQna5/REDACTED/eTOz/urX+18u2pv1zKqOW5rXW6MKg8+pW+A6Qn/3p/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QYQ35gOM1kQuHlSo/XLQ2/GMNI8H2DKO8Sny/a0tcHv610V/REDACTED/REDACTED/REDACTED/Rom67528tji8YdOnP7y01G/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/C9mXy2mIvqeC/REDACTED/irGIUhOu9Wep/DEKvM/REDACTED/REDACTED/REDACTED/REDACTED/3z7fKXdgY5LCDV/O5hI4COVPdkurkuGdSmKZ6hCkwci3YW/dnPd4Pa2+lNOwHfLl/REDACTED/jePihrOb5/UM6DsxzrY3ySWz66pJZc84f6KJe8xzJ33/093y8/REDACTED/REDACTED/QwJrJ/REDACTED/REDACTED/OlmlBVi2U2O2n7RkAAAQAElEQVTub/REDACTED/4iIna/REDACTED/nX9PoyXNpmRnkR+G8ZZN6GiGs93P7K/XizJ7bvjMIhg9Zgs/REDACTED/REDACTED/REDACTED/REDACTED/YRSnyiNTwlyOB/REDACTED/lg546BTZ5/REDACTED/9Ou0EaqPR8gfL5j7//REDACTED/vTFpQceyu2Rn/7gAH9fXttvz29vP7sfytiJ/s/REDACTED/REDACTED/REDACTED/REDACTED/VaP9X98/X2UqWpq7hip9lBeWJ6cvQqlc7T/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/iYQ2rT8M2EHbJQd4ClGQl/YNerAE2Gqbnwto6A3W7Zmti/OdPlCqhSU0UVkgUFObi5Qcr0rUQUdIXVF/REDACTED/REDACTED/REDACTED/nu/m5JmWrmO/REDACTED/8tUh5jf3ZG401xH6GrFtp0h79/Xt8re/REDACTED/REDACTED/7nOg4b0xbLW3+2d0FXYmFCZOv6d/TvPdmA4AqO9sxyStr/REDACTED/REDACTED/REDACTED/REDACTED/ZErC/REDACTED/REDACTED/b1MdSRMvIRnwHJvN3oD9M1LtRUpG/9D2ulwmA/FonQbu0Z2LLIBQUe7+x90IIz7jXy/REDACTED/8MpJM0u7ydArPy3/REDACTED/Tbr3Z2vvO2vyx6//Trvm2T76LVceeEESFJnf/BzaGhE4I4inHeBN/bvJ5yKv8Bx2hI/9SnApVzZXJAG4vDkwIzA8/MBm+gc/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0eCIo8oG9cxif3L/REDACTED/Z/REDACTED/12/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Cg/REDACTED/REDACTED/0cno+TdelZ/fN+KER/f7ISbIdy/X+zu/U373dngy7/ch0AEAkMqSV4jnv3Y3HN47DTrS/Xz65G/REDACTED/jDzz//7nfnt/REDACTED/REDACTED/REDACTED/ZI2ZTjTWJgcJP4/REDACTED/REDACTED/dqtMos28vRya+1S8/fT7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/Zc2rjJfg72XIUDO8/REDACTED/68qVdf/REDACTED/Di8WOJMIYvL6+Xiztj/REDACTED/REDACTED/JA73WrITppO5Bua/aIGhlopI66OT0n0kvl/nVebCUaffZVN/REDACTED/KV/xrF46jZax/REDACTED/S4yjGbpP1TOvHjYwFaaN1/REDACTED/REDACTED/LhlsoTWqwKMohCbegPDs/rcO79we7E6/gU7MME6OdA1ULe/REDACTED/REDACTED/REDACTED/vAQ/REDACTED/Th36QSn/865f/NBHiJND6XYntyTUOzkWn+CPXDzlB/+Yrj+o8O5I1/+Hr1Ol/pDXvXH/r8P/w9b9FC783hst1qCpkOkj/G3402XGby+36+z/8oV3//Jd/REDACTED/REDACTED/NXuFoLmMpUw1cNUNdIHUWo6zOGkkuu/PvXSvavXAsL2b5V3R7uU2G/REDACTED/REDACTED/REDACTED/udSiqmN01y4Zqa10wOl/REDACTED/REDACTED/REDACTED/r78q3HPbj/REDACTED/v6/REDACTED/ySzy8bZRwuIjPKUXR4pijly+/REDACTED/REDACTED/REDACTED/3pPuaxaCNCyoxqxTaDp0C7yzH0lHfj/PQa55mt/REDACTED/S5+FJ+KG7Hyse9GPXhTn4SPlhnHCs/REDACTED/REDACTED/89NOn0+nnb5c3EIHy5adP7c63y9e///K1icv/+Y//Q/REDACTED/WeaCbnd9/REDACTED//nM3BESVgbL3VDPiRYgDXvjCGhx/REDACTED/REDACTED/REDACTED/JEES9DBGLsm6c8EK5N0CDjPFyN9y/REDACTED/fNeX2/REDACTED/REDACTED/nLNtyTdRx793Ge7CBU4C/REDACTED/WZan7JroVl2zfVK9oW9NRvrT/REDACTED///REDACTED/NRsl52/REDACTED/REDACTED/REDACTED/REDACTED/XXZCWyaVTwn/REDACTED/94MuU48tq23iG63b/EY9y5J7JpsZTKRmC/REDACTED/+9ZezU/fy80+vbxc4F932T6+fIfd++9d//REDACTED/r2DcSonQyfpOk63756hgc/T8BNXL858Mfp9fTTl9dPP/kR0s7hb18duqKpCX7+aUOrM1/REDACTED/46gvh2dV3Pp9wo7MBl/T/REDACTED/XS0YqTutq3tL9U9c/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/OKzylwwqtYKqvkDAhf/rObc86f/REDACTED/REDACTED/REDACTED/GRPSLBK+yWd3V/REDACTED//+Tm88lqOsfhgvfaj/E5bL512yawU7rLD4Uc/WB/NqdmEyZM6VNLl0dPun3ko6/C1/REDACTED/REDACTED/uf/REDACTED//REDACTED/REDACTED/W9TItxMefR1/pVKu/REDACTED/REDACTED/REDACTED/danfbPRaAYfh1ab/ldtQUdNejPsd/REDACTED/Izlfu3x2VRDqubxGX5lT17exxFz87B7+8qe/REDACTED/b12/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/XWu99zDnX3mufe29FsjL3ueP2NeaYY/REDACTED/gr3VC/REDACTED/oAio2rgdnsULl9uX+SI/REDACTED/Vby2t1Ym6Ot28e9OfH0/REDACTED/REDACTED/8CK2tMu6UFa7OYucNe2F3I/k4L4v6RxfKHX6QNvGTtrPAOWqf/REDACTED/hAj3QZcnDHAWVScNIjxqyNvTD//U2F0o7HygXX1Qa1QMAz2H2Ki2pCK/BtbyyBwx7zU+/REDACTED/Wnna3t17/REDACTED/REDACTED/KFnZD51BNr34iwPG22fE8g/REDACTED/REDACTED/REDACTED/REDACTED/tNMQDN2HqhXYgvlcdQTC6/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/B2S1nBJdpOxZa3LcmCaYEaF58ORi/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/jPix/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/momGEZs/8n8ny0AeE5O6HDfKg2tgumo6L/REDACTED/REDACTED/REDACTED/m2Wet97NypV703/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/4mVj7pWkIyR9gIHsbD5Zg9TIgpjwi0ESjMsgIm/iBa4Cl2ATANlchaX7t7+cKO9C5A20ORXnE/REDACTED/BC3SY+eMCLX2zHAwYxlwdRfBbw/CiaXUPkKJH8/gej3/Pmkp3VRI9jg7Wtunb/JZuXV51/x3MEVuR/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/So/REDACTED/z+bCl7DQTNx/REDACTED/tn/REDACTED/REDACTED/OqV/REDACTED/REDACTED/REDACTED/t88nvu4PGnh/REDACTED/REDACTED/dWMWi1Njapm/REDACTED/REDACTED/anLxrsL9BYUZ/REDACTED/REDACTED/SRXYHA8E6P/REDACTED/1ct3PdWfTvnC/REDACTED/6u81BMiOb9G3fNsDfQfGN4t2D/m/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/yr0tWhKcLMTCOVwlp/REDACTED/REDACTED/z4dP2ngrgDeD2S1fNIx3z5/E/x/REDACTED/1r/REDACTED/REDACTED/REDACTED/REDACTED/QAVSU7d5/REDACTED/T8Shdj1VVcL+gn3r+cDh8f6l9X1fDOryG3/UiLdYSrsvA/REDACTED/snslwzSoIvn7/ZcUmZ0AiIMQs/dCrOZpwL5pA/REDACTED/REDACTED/M/REDACTED/INTA2wVDs/REDACTED/nGZ1J+GrVJdFJkf8qO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/zbLSgVp/REDACTED/REDACTED/ZUZia/REDACTED/REDACTED/REDACTED/LxD5anVe5feT+T/PTvi5aCD/hkEQSiuvo2KZF/REDACTED/REDACTED/bERFkIQ/REDACTED/REDACTED/REDACTED/REDACTED/XH9+2l8eUrtqpv87wy9vtdHk+GPlr2/REDACTED/jCkTB0AQxwe14BRxTmrvfZPMi/j07v2TwVpzbM7TbndQs85Rteb5bnenK/REDACTED/PysUPqzt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Nn2ptIceZtkEOAPAA/REDACTED/MTGs8lZ7gd6gWbAWsTHGZI/VXaDhon/REDACTED/REDACTED/jpgkQaLBPRHs6TNiSnUqaMXq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/n1Q8FYg/REDACTED/REDACTED/REDACTED/I1O0x/pikjg+ke3I+z35ouYac/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/c3d1ZTqy1UqfD/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/X3FkhSkjMjekQ67/REDACTED/fK5/REDACTED/EpS2WuXI3iQH/REDACTED/REDACTED/FFRPv/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/+sHj5UPrC0dpxw/dCv8r8pLYfmukE/REDACTED/e9A9/rzff/REDACTED/REDACTED/errr08nGpE2kxmHFSE/I2BYHr7zndXWElDPJan1C/REDACTED/CrWZki/REDACTED/REDACTED/REDACTED/FbcpXGgvp/REDACTED/REDACTED/REDACTED/aoz/REDACTED/X/m08+QbggalgTLAfKVG/D31sZ2ud2WAFet/ZFjTjfq/b7Ulkq9RW/REDACTED/REDACTED/REDACTED/C2lCClPdKCtUAR0OJ/REDACTED/REDACTED/REDACTED/zWbHfDYpwAfhs/43wUiAPE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1MJ0+0PROOhsOtx/REDACTED/REDACTED/lu0feajXYP5SWOE0efL89XftiG/REDACTED/mRTV+slAAZONJ2u7OwuuP52dJGzaoK/uxbb/REDACTED/REDACTED/REDACTED/REDACTED/S4X/REDACTED/REDACTED/REDACTED/xo+v3TY1Vp6Wm/REDACTED/REDACTED/bPaghT3bq3E/UZZ6eGgErMaqTZWHGU+PT0/REDACTED/fHxyYw/u7u7b3++3d3vVhYrWfT2h5N5Imn/REDACTED/TjO9Ujj/itUhzlbHeyRP/REDACTED/REDACTED/REDACTED/REDACTED/oBNvNB40ny9BGR67XuQPL600VuLe13V1k3I/REDACTED/REDACTED/REDACTED/hcClJkraIyaoVJmpZJY/oTE0cZ9EXRXaBb1tQx/REDACTED/REDACTED/H/vQggOV/REDACTED/But0fXx4+2+dux/REDACTED/REDACTED/o7fFbShN6qxthTodbqtVBnPL1UonZR/WZ72xVpdt/va150GLJF+u+dyI3bjaUxPVWy/DetME50HZd4OW+rf5Y/xCbpwpli3WDL+Gfu/vNn/Xf+Q3/Yf+jt/4oz/y49/+9g/toqTW3zKflIYAqH+f7vCD+zw97X/lV776hV/4xb/0F//az/REDACTED/REDACTED/REDACTED/bz6TJ2Or3Oerm0ZH6Pn097s/QJ118cf3U/L3Tk1lrC/DIjH9RIG7g6Z2xIy3Ixrba7rSpGVZ/7/REDACTED/zOSNfZTFfZUW4J/REDACTED/REDACTED/xQQ7fRLfEdLBnjlqrn/4h34kBdZyEZGKhJz6ArmcHhm/REDACTED/REDACTED/8RM/+rt+9+/+z/3n/wvyH3z+Vvn89E//zB/+V/7oX/rLv/BxVtAwYKyfuiDKXRaT6/NNNh/vWW60LxI/18X2qy/REDACTED/RkBYAK4WJcUBAG5Gcy/REDACTED/YjFcDKxVAkYZhhNMk/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/gjm0YF06JjDWH/R0W/REDACTED/TdrsrlnPy9Lw/KEGAK7Rt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/p1GHYgRAQlGEr+j1N6fj7/hv/td/ze3+v/AefvxU//9If+tf+uT/REDACTED/yMWuo4iH9+uEafl/REDACTED/REDACTED/yCsh/REDACTED/REDACTED/REDACTED/IM6YZn/REDACTED/REDACTED/tCYwTP+LmsC36wC/0L5lnPjk46u4m7vmjsB4kHi/REDACTED/REDACTED/EBLKzWJ7/REDACTED/REDACTED/6I5//l/7Bf+BHf+zHmhj+13/+3/4Lf+HnfuEX/vIv/eK/+/z0yLozTuVy6MrB+MRV2c0u7e6O/REDACTED/REDACTED/uL49s3uR37kh/6On/jbfvK3/F2/4W//0Tanv/Dzv/gv/p9++t/5G7/REDACTED/REDACTED/REDACTED/nFCYNzz9M/pgsK97EsCzY/cI+iYvo4FoC+sIF1/REDACTED/REDACTED/REDACTED/8tio9/REDACTED/c7sa36/REDACTED/cHw+H/dGq+JoSOCMb8xn1eKedVcuVw/REDACTED/REDACTED/unxoLwOEcH6NHu/81ktxKfP73892boV/REDACTED/REDACTED/REDACTED/D8ZK2X9F5E6Dsoee/+7f8xP/of/rfe/PwwKf/yX/jX/+//p//xZ/7uT/j0FPGsoWpuhY/REDACTED/REDACTED/vsdoBrhFU+8qa3j7/17/lN/9X/yu/8e/++38rJfff+6X/w3/9f/7k/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/28xIA/REDACTED/REDACTED/k5/q3xGScP+eW/REDACTED/6EKsiUj5xmmU/REDACTED/REDACTED/6J3/Dr/hf/q/9JQ7//+//tH/h//JF/REDACTED/pq8yzWfuWQ4j/5+1NPwpONPuCptYOftiQl+W/REDACTED/3f+Yf/yf+IT5cMfA/+vv/Z3/pL/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/AMd3F3BrZw6dJkrIvsIdKZMG/REDACTED/fivh15/REDACTED/t65+xVtg+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/d2/REDACTED/Ud/34//+I/puaenp3/pp/4Pf/Xf/ksNgoeEINI5vsuBEn+2J1fXZtk/h9d4iLvfRduLa/kqid/2Nn/b+t9h7tBO17Dnxba/r/O7rg/REDACTED/tfZZ7mstX/dEkrNaq196f2ftaxn/XldxlicetH3ve6HYvg7/yNv/73/Td/75uHe/3j53/+b/6BP/B/jOG8+s3Fx7t54/SH1vdyT0rfOR/REDACTED/NS27+bVNT3UA1/REDACTED/REDACTED/REDACTED/REDACTED/G+JI/REDACTED/REDACTED/REDACTED/j89Nhf9TNdn//REDACTED/REDACTED/toIleT6V/REDACTED/RdP9/REDACTED/O//B/6x/8vf/F38Vz/+P/4e9/REDACTED/REDACTED//iLz79az/9//1n/pl/iqeVvv5zf/REDACTED/zWc/REDACTED/REDACTED/REDACTED/REDACTED/5yDc4fo99eNXxI296zZg+/r7tzOX50UqZaw/svmG9HI+f8k7fl8/1na/REDACTED/FgYTG6H7dqzJ3Wqot+frJ/REDACTED/QhmTOSLVuir5AVJHE+Pj/qT02a7M/REDACTED/dpaT8xBCAJCxzDqAimsNOEJ4k/kuidQC4FeQvSrP/REDACTED/REDACTED/Gh7Vql/REDACTED/uD/7n/O9/rf/LP/y//nH/2/REDACTED/REDACTED/96m8zO/rQME8awu/REDACTED/zn/3H/4nfx0n/ff/QP/UX/+LPL9fGzTaQXXlpiJF9t/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/75yczC6+yaYWVLzw9v98/REDACTED/vUOWaTURJ4PXKyv8q2Tk+d07Fv0TmK/REDACTED//yKm1Uq0vdmTAdf5Ku44uF7/K7a5r96OSUbY80ky++/REDACTED/REDACTED/REDACTED//zB/7E/qjf/Mv/Ny//C//VNy/REDACTED/REDACTED/REDACTED/Bd+6g/fv5l+8id/o97pP/qTP/6n/+yfWd4tX/REDACTED/REDACTED/g6ro692/T4/P28IwaBhq/REDACTED/2UImQQOesV/hz28wEOmWeAAO3h/REDACTED/REDACTED/54H2cz44dFMNNnC3VgcJhn3rgCm4DbCnc/REDACTED/pk89M8/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/NqnfW5en6/REDACTED/REDACTED/N1pY6f/REDACTED/REDACTED/ov/V/81WBEjIo/pf2RAmO0dj/REDACTED/REDACTED/7B/7/ezTH/m//REDACTED/9RBA8d7nmHV0NDyq/bwLb0kkyUgNJQYkjXCnW4NlXJfD/REDACTED/xvrfOX2Hkn/vzP//f+W//1/Wy3/Hbf9v/+//1Zx/REDACTED/Gq/18sfLz/REDACTED/REDACTED/URJpVPF/NcDaCZI8kkROTaOh/REDACTED/REDACTED/REDACTED/REDACTED/iKnSRXsQmG62ZWxf3T/aubn0yA+oDnBatAemmJcMcrfd/dof/uF/95d+aX/YB4iTJkphwqXtl94OgS/REDACTED/u0PT9WyOq8f3ux0ix2P8/REDACTED/XaptVeGmlC9/v9wpclX4g3VQ+Hk6PT+/1FbVLDw/39/e7zcZ4pzKo9+/UHDyTp+yQ2/l8Pu4Pz5Z/a54VIb/5/REDACTED/REDACTED/REDACTED/f9PbxAzb//vz//J32KaTII7aQsiFpHwzUc/REDACTED/6KSuTWZ100wO88f/Wt3qtEUqD3mbQLKZ+Pl2MT+2hZlcoNrbZZftP/+n//8/93F/+zb/5J/QOv+0/+R/7I3/REDACTED/cI/fDGntvzafgRNdX0gqd4wrbf3/REDACTED/1sWTmJZYZmvvWUW5wvwbNXnaEQiN4qbDRv5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ny/zjeB69bcxYL7wZz/REDACTED/REDACTED/Dx66+e9odj1EugM/b8/REDACTED/REDACTED//REDACTED/REDACTED/fuXAzLAnLjTTu3C7hzvUbjPdZ/PXy+TY+/REDACTED/MH/vj+v0f/SM//REDACTED/REDACTED/ONVJTtAf/8P/9Tv/N3/REDACTED/I1tPQgKi5slFCXqt2nna/REDACTED/REDACTED/REDACTED/lME7kAEgb1TiVkpy7/REDACTED/IzGL7ezYVjGddYZkoS6AF/4IS/REDACTED/w2DWwhuh7bjTO9Ql3pwMfB/7+3tr/B0E5piFp5ud0BYVraPDOFaS6OFi/REDACTED/AAMP59/REDACTED/Xa9u0J4vusdy/b95sFOPqZlCj6/REDACTED/2bB9iQJ9MIp/REDACTED/rWw2SmZvPZVsx/REDACTED/REDACTED/V1LCpg4QOfZNcPJjfWomUv/8f+J3/4d9oNsA/+tM/9Z3Pd/REDACTED/7PPbfX/XG+WEiRa6QYkPGbRlVqW2/REDACTED/9PaU9+5If/tv/bv/r/edWSvUbqyyTHsoTZA2a/REDACTED/N8eDQ8alFOE2WigHIGVk/REDACTED/REDACTED/REDACTED/Xxni4QlM/Dc8oniepuDwvF+f501I7gymvOF/LwJBKXOrnfaLakfupxJns6rESr+gaxfYDe9/MnCb+A4BquKdkzjZ/REDACTED/ow9Om7iNHWbRTu/REDACTED/REDACTED/dKXBew9tZ7/bu/REDACTED/erazQ70apLrygT1TZrNeWX1qpw/Gwt/RXz5b7WbHz3f3DZJmxdkoi9F2f3z/qvanbZnrMw97SVeq/S4msbe/REDACTED/6GciPEvsoCQNeY/REDACTED/REDACTED/9Nf9On711/REDACTED/REDACTED/8pf+escpR/9sR+WYW2kq/REDACTED/I7/REDACTED/REDACTED/REDACTED/Db9qoF/OCKEhyhrBfRofjm+r/StO+YU1nojsKvKW4aHQ/REDACTED/REDACTED/REDACTED/Xy/PBX9OyPzc+5I6D0WMpqIuLTT6NbM/REDACTED/REDACTED/REDACTED//KzcCLRkdbfT+1neByW/T48HhawkVfqtPkm39/REDACTED/FpZt65q5SEC72sdvMMe/ASSxbD3kq+23r5UVTzuf1k5DqgKUk/4sVAbHcfuCJ3cbS/1TMjSYIznhf7lL/767u4hdfg60ou6pB3iAtfVUg3ucnMhX/REDACTED/REDACTED/9Sf5pz+1Z//REDACTED/REDACTED/L3XE1Pq86BtGBkIcHPj1/YQnA0X7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/iBuIek0L4OzsAbEzL57bxdh/NVFsd0daafb9e7Wjj+Wtz/REDACTED/3/ZzWEvnhN3JqC5wePddHu7zW0L43C/REDACTED/Vxqp7EvVo/rkzQaJrJRunE/REDACTED/REDACTED/9/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/dm7vTwNpf6JpilGEYSiNL/REDACTED/REDACTED/2B+S85y8qBUdw3NYfTk7/REDACTED/REDACTED/SvLdgjc122XPoZ2XbTb8L3c/REDACTED//4d7/REDACTED/unR/REDACTED/Wk/ds/REDACTED/REDACTED/REDACTED/pfewC/CdZ0Wf2mpcnndiHYV32/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/JsY7lQ+Ow0cdlV83VvIDPx7Ph+/+yq989fVXjCT4yPU/8H4mCQ0TVERgPeBNp/NB7ZOsLaS0T+2c798/W3qnWk0NubYc7Pvj0/REDACTED/Pah6Gqs7K7d7dbc0LWk5qG37emyWZ4h/L953m4/7dk6mc0Qe1A+vjjCWXcjjNh6/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ZVjTNbromziWtozn6wVhuDz61n/p2wvys2zr3kcOcPvj/eN3P/SYq2NNL+V/REDACTED/REDACTED/REDACTED/ugMu3Z2LP5xrlAmRzGigZPxk/REDACTED/REDACTED/REDACTED/4mJZPuXW8CaQ/+qvLp11+dLN/94svbMlOK/n4p7Ph70u7i/t0W8mUZFH/fW2FgLD7WYLIQKlYudrT/REDACTED/VJOvZXtObx7eWlmhSeGreUorxdxstm/REDACTED/fbO7293fb63a/REDACTED/32tz6zxNRZbdRrRe+WZrzKbrvTVbxVO/VuYxpqe1w6nsphf1ZQ/nD/REDACTED/35nROAyC/REDACTED/REDACTED/REDACTED/gdBQZ+p6mi0Umj2LWbRa7G/REDACTED/REDACTED/REDACTED/REDACTED/3E5jm9+SZPJM+Wi7MgM2aWDUj/REDACTED/REDACTED/bt3FVWCdrvd/REDACTED/VaB+tdfv4t1Xnfrze5urW/xjJLEz8/75/1RueX9/REDACTED/O6itk0jQsHxfIsA1CXgF1b3tz/Mc1eHmurUnxybfSxA/3b4WZI3rPah0VahfLpAWudh/REDACTED/REDACTED/REDACTED/QhnRdz3KnGYf8lVEAu/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/uYzyFN7UvoOZqK/REDACTED/REDACTED/UlitIi+2q6tueru2G/S2S9C3286kF+3swmuqvfZvYsa/QhGt9jZZeOGSbfdpfRvehat7wRQ/0B71BkzMO/REDACTED/Nc6H0jD55qEluYSwEpDA9/REDACTED/fPz6wzrrZitalmywxZH98/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1YwoNjbOcb5/REDACTED/REDACTED/REDACTED/v3X/6O3/Gf+K2/9bdUCWEIgtXP/PF//c/8qZ+9v//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/cHzqdPnmlJfsR9rXx/REDACTED/REDACTED/MxXe3/U7hUuCicmjUmLwWFQSzoQsB4/dC+OJ/REDACTED/fm4W5tnsbmHqxoVjfGZrt+WD/c3a31cSiLy3yMK3NgRm5n/eHz4VlRpdL97XarUDxZTuzD8/REDACTED/qNB8tfiSJqm9VY/rt77xZozreerVRO/MepYb1TjpuaiS+u98ht/OpgGA9PR2U27x5+4CygpP2wbD3/REDACTED/5zXD7vPJfUSR20bpRAG/Aw+tcr1p+nxJNZSW/REDACTED/2Txfpcv9vFzna1efm4N1fj1y9/REDACTED/REDACTED/REDACTED/8yt/85V/5+X/yn/wXfstP/uaLOf+tf/dP/p7f+1/+sdX9dz7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/LBsk4vj/REDACTED/c1b7rh1v/REDACTED/0kve7B1Z+VxD6aIG+J/gOGe/REDACTED/REDACTED/F++51kSsQModsDf3E1qGZz/REDACTED/REDACTED/3lVlH395c80UebDHyUmP/8Lv/Bn/+yf/8N/+F/5C//Wz/7Yj/REDACTED/buapabTMrODCLWRpksxc/REDACTED/REDACTED/REDACTED/DxHHiI4/REDACTED/+RGipY5hx9tDrnKJEE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//e7rijiUs1UGXm13BpTNlyWl/f6ov8CaTCxNvN2u53L84qtH3YCKb/REDACTED/REDACTED/REDACTED/omkyCEpqQ9otiCpF/RbMtS+l5g4db4ETJ+T2+GN//E/Ip3x+6Ie+/Y/8I//wX/93/sY//U//s7/0s3/REDACTED/k+kvCw8Pu4ya2JCipGTzS5FPNQ28/z1Myyx6Ppm/6NP/mnvvvd71684J/78z+rXx2PT+/REDACTED/REDACTED/Chve8oLrooUtIKZdm3AJ/REDACTED/REDACTED/XyKNKPQaG3qUs9/wizYk27xzu6O5DIFG1uIbQQCUGs/REDACTED//REDACTED/REDACTED/OWfHrW7aQAeYvav2qnhZLOumqVeI8n7b7ab/XUneVtRlFfMMvTqaj+97Mf+mwFI/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/G7LfuzKoEVXtFEMpLm+F5uVL/REDACTED/nIur9QDd/q56te/hVf/41/6fWvf8PnfPYnXbx4ePNyL186/6O/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/S6NAiUS0bZIARxd+N/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Mq/REDACTED/ealO5ksEdbQGR3XQtz1/+CP+/C//88/95z96y+/9/ts/REDACTED/0511O3qb989H5zHA/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/a0FP5EZ/Cc2kA8/kDOaU9+0PYM8wdOGfk7/REDACTED/Zd7TnuiGedz/RusbbhQKqSLiA/bDRlmNi8WYHr1m6/REDACTED/eab3lzeWqBbbb/2td//NV/7Db//+29/4QvvzTrPzoQJ/REDACTED/vzCqC5jryc+zhed1Ftb+/REDACTED/XrsoIpSN3V29D/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/UikEPKajwmVM2q95jag/nlx5Ofx34lTFfdYNMett1k004k+BnD1I/REDACTED/REDACTED/7d7fyya+mHqsUsrTNQxLjK1Vyo/62q6A1mSRBWrqRWjl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ZTtcf/ZOBl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Vsk+/REDACTED/REDACTED/mYF33C1p4v/uI//3M/89OXLh3vHvxFX/iSf/zz//REDACTED/4kNrgLo0q8+5fXx543vPk/REDACTED/REDACTED/QGAc/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bj3LpvXabtp+9auuaJW3tQ/BC7+b9Isy82/Hn5CWWwpMHJ2/9dt/WFnK6SXz6/REDACTED/REDACTED/REDACTED/REDACTED/liw/REDACTED/Ew67jcaA1wFk2a66vrga6xrheaXb4omB/p5xbe8+MnH4hhKJFJpElj2etrUS/REDACTED/REDACTED/Pobf+MzXvy5P/dzf7/YZnx7x9Pv4OMffOiJjVRl2/REDACTED/uV3PFx+BCMxLiyWLmc1ddz/REDACTED/REDACTED/2vDYv/REDACTED/REDACTED/REDACTED/iYlePZ1WR/bPZ/m83QzmbnT/REDACTED/OqOdytJLZ/REDACTED/REDACTED/iMyWn6kZ4evMxSqNo3oq260ZZuuCA/6fYmrrIXVJ/REDACTED/REDACTED/REDACTED/ocTm5ru1WlA4BzwDKBsSRn/REDACTED/7EUNNdBIVCuB9fjMAzmV/ZWWWH69Z5uDpfX2t5mf/dQZL/ev0s/77crp6qmWehg2be/REDACTED/UcaxJPGtSgj08TRU4ieW3/orrWAHhfwiKk001P87vtV3k6/REDACTED/k7/wP/5LbLF8nvgf1UDz185fJtz/i6r/3aL3zJF9xxx9OsWujOh7HxW9761jf8yq++7pd/8c6nX3ra7Yf1rDE85u+F/P/HHjt96NFr3/REDACTED//IFXvvLr/+tv/Jq99/+a7/jrv/mb//6euz52Mr6IZy9Tb+tT3WOq1P/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/BcCjLJq39fyh2h/KfvP6Yn0M+UK53aWd/REDACTED/f/REDACTED/VxCloNOx2jKIoemm2/A1psJPNRxPhu2aXbtLBM/REDACTED/REDACTED/REDACTED/REDACTED/IYC72daWd/REDACTED/REDACTED/REDACTED/o0wcmc5xATOC6KVTuulA6wH6bqtIj5Db/REDACTED/REDACTED/bH97/0y1/6L/7FDx0cTJ/0KjzNGYjyf695zatf9hVf9Xu//66P+9hnTsbDWrr7qiSPe/X6/O3vevhlL/vKN/7waw8PD25wZhZoX/PVr+D/3n3ffZ//+f9FDBfufeYLRackOleO54/O4Nn86vve/x+/8Ru+7nv/++/REDACTED/dZ3lv8+uM/5JiyaEfo/REDACTED/REDACTED/1/JonVM0qbsQmdLdWFR2hLEGz/REDACTED/QXOl5w/REDACTED/REDACTED/vut1/REDACTED/ZzOUfpzNzyR/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//HP6Bb/Hz/93/v933/a9/87//oRR9z93QyhGkiS11WMp544vR9H3j827/9VV/0hV/wH//gP938mY8vHn/w/REDACTED/zMF7/sZV++t5ceefTRb/mWVw+Hh7ff/REDACTED/GfWMeAY0+/mMoY69oDub/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/HTIKy2Xs9ikOeX/LXuIsAABAASURBVEIhPRjyurverEWIt5Luy/j1+HiKCnJDdkfHKEHUm7VUYBoJTTw/REDACTED/L5ideOhuoD1WCjf4R81C/S+EGh8denY/KunZ4urV06/7Mv+4pf+xf9q9+Cf/ye/wMffccfFi0fi75UQj5Q+5gXP3x9c/WSf33jjrz7r2c9//wc+/Bl/+nkwwkIR4b554MEr733/Y//oH/REDACTED/+DP+7K/9y1/eG7z9/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/RzG9YS3Kx4SUsyjsrspiY6/IsL4lTORXh//VzJdXgDL0ystxQ2E0pTq4fz/teYGJ+nvytVKiG33A9nz9lKdie3h0/Mx7n//6737tF3zB5+0eee3a9V/6pdfddvkI6Lc/sJ7Kh0Xcd/zVV//Ij/74Y0+c3XH7Ibn6dna6fPu7HmYQ/hTQb/3Jq+6ND7t67cEXvvCj3/Arv7QX/d733vf92U//7OVyeeHC0wejA+t/dUbl0e79bz558mOq96j3kecRVe8xbN/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ALB49vsYrUAWMGb1Di0ew/REDACTED/r/hwCh/1+J211n/REDACTED/REDACTED/nshL/REDACTED/REDACTED/f8jmrd3jqdcPKifLnmJDt/REDACTED/noYwcCYF+E+18/td/9vO7O3/rTXvCgH/REDACTED/REDACTED/zir03jI/REDACTED/uv1pt732td/3O//+d3ev8uCDH/rWb3sNK7GHh5dvu3TPfHZVd++F/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/cZbkMG/m0/REDACTED/REDACTED/BB4UuZ4RocuJRR8qlRYd3p/KlbYGUQINaeKcRleX/REDACTED/REDACTED/REDACTED//S9gdLqci8CmxUdqz+/p3tze4/573UoBehNhaUo/REDACTED/avBslSYM8qW1aHw/REDACTED/BTaEnhET/REDACTED/REDACTED/REDACTED/on3qfO7qr3dQm8/cH2I5/REDACTED/REDACTED/973f/+Y3//YLX3D3PXddyrBhPl+RhUDLmd/5rnezO/d1r3v97hl459/63u/5rr/+Hbtn/oZvTKen89uOpwBUT1yZnZ4tvuWV/w1j5r03w4Lu677hm/7Vv/o3ec+z7733677uq//ad3w7S2r+JwsoPu/hwaXhQLItrg4fpXNDoNe333b5P/3B7144Oty90Lve/Z4v/REDACTED/REDACTED/REDACTED/REDACTED/hyuUJd3Y2my/REDACTED/REDACTED/C9EPh9V3KoErpbO4I9ux5SHL/REDACTED/OjXBmq0Sp6V+55tWH6sOD3mv/Z9Kn1KqDIR255aCVL/mp/jhR/iVX/mXP/TDP8po8Pji4T133ZYwqnWJZLj+0c9/xr/5N/96Opl+3w+89v77H7jBqf72a3/421/9bSwf6p38/J/yyZ/0B//pD1nUjEcNn/X+DwlV1atf9S17T/Lu++773M99ycnJab3zAx/84A/+0I/+5E/9/V/4J//LF3zB541GR2RPngx1nfMZjUa/97tv3ot+3/HOd336Z3wOS/iLF59x110v9CXOlj1vp+odddUxKR/jd6H7o7+x/A599uTrmgYWMDLdcdTbpvLLnW9raYTvKY/REDACTED/REDACTED/MwAn1ROCkrHi+xo86sLou2s1qkPH/REDACTED/REDACTED/3A0Jjf6BQ6X6hwEvq+zG65N4Jc/REDACTED/REDACTED/YbKE098U7+hsfOcjEXFoV1y/N3OBhFhX3s/1xeX7B/REDACTED/iSAykO1C0WZ/REDACTED/REDACTED/REDACTED/REDACTED/ddOFuV+LG/REDACTED//5dsu/eW//M0/8Ld/aDgKT1w7Q5SgGx/Z3Tr5zd/6zV95wxvlePV4HxyODyZDJTuIx5eOx6Mxr/HXrgnN+2/8X//6ttsubZ3/rrvvCn/4Rx9+/OzgYMTnfPzKjLWM977//e/7wAe27ofv72u/7ptOT/kegpRDn0wY/SyWCxY+JMQHZ1/20pcfHh6Ox5ef/1GfulidadRnWm+WQUKg/zCzQJfnFaD7zre/451b+9///REDACTED/N6/OOlwGg/REDACTED/xpEEnJJ9y12tYpiiZW/BLRGdT1lIWsDUJrq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/JGvNKWy1d/qH+n1V76fcQcnup7d/REDACTED/FgHsfBVPphbrO5hMRhJ4LB/REDACTED/REDACTED/REDACTED/REDACTED/1ZT4WrmT+f9+c+9xu/4eu+9uv/6ze/6bc+/kXPPDgYl7khISTrxx+XrOBP/sQ/9be+93ue+7zn3Xb58qFWGr+Zk/+7f/ebv/7r/+dk3Fy+OGapxjj5JS/5/M/dF639+tf/REDACTED/c/8PbVan56enrnHS84nF6Gg4h/dXXwSJIQ6E/aDYHe+3nLW9/2F1795SzYLx3f84w7X1B1bX8dyp/REDACTED/OySYRtNOMUH9CAa7rpCS/gVO6t4ahV4D/REDACTED/i/REDACTED/REDACTED/REDACTED/REDACTED/jAQzGE9dveYzfbjjttuuk25bdje/REDACTED/p6f3j9la/REDACTED/REDACTED/REDACTED/lYj1CQzmU/REDACTED/a1baqkKg5i93iFjjFkVvmQPIyP3J6qSqKKf/REDACTED/dr2/REDACTED/d/REDACTED/kua+uf9+h5n2vXrue2MBP0Q5Srr8b/x//+zz/jxZ/773//jz/rxR8zHDawc5+eLh/58LWXv/wr/rvv+W+f+5xn061/br/9dtIClfwcLGi5/ac/7VP3HvmDP/QjvP2Ej/REDACTED/82yy4jg5ve8YzXpCdOL1ZTD1o5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Hf3bup325CrfTLulcob62fe1fSUFa/REDACTED/ealYCVvX1ClMKkEWi8l05U/REDACTED/REDACTED/REDACTED/REDACTED/R/i8f1/V3vGAsQSTvXrdugTKFY7zd7g/REDACTED/REDACTED/hy6j/ecFHP/9V3/YtH/VRz9294qte9a2v/NZXv+OdH3rWPYxawyOPXvnQI9f+9vd/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/GuHZ4Ko0o1S0IdrVtnbvovy2/REDACTED/REDACTED/Wem6Eguk0OBK10jBR5KCPSlCxN/JFv/REDACTED/721/y1//kf/uzLX/6y3cN/6f943b/9t//PRz3v6deuzj/08NWf/REDACTED/2T/REDACTED/Jn/JnT04fu/REDACTED/REDACTED/REDACTED/REDACTED/h5eVCMY/REDACTED/REDACTED/H8BvO7eBp05hRQSu/REDACTED/VGo45x5BhrfTayrEMwelYmiWz54/REDACTED/REDACTED/REDACTED/yL71Zs3nPzqcMEwXn/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/tI0S/REDACTED/M/6nmvfvW3/vRP/REDACTED/W/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nFdw/REDACTED/REDACTED/REDACTED/JoQxqs+ljb4Y5FAycuAy/REDACTED/yPZRNFeXbLZojOCCPL/REDACTED/dd28df3omJMyPfPiEt1/5lS/be06M//sfePAtb3nr448//thjT5ycnPDt/bff/Z1C3dz/vPs99/GpZov1lWtzlhvc/p3f/REDACTED/yT/REDACTED/REDACTED/MK6tjN3qfdKb/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/qwXbx3/vOc+57u+629KPkVKf/XbX3X33XftnvPKlauf8EmfdvXqta39n/WZLz44mG7tvO+++/hU08mA72GtSvblS5f23uptt11+/REDACTED/+4i/92I//3T/4/d/excCvf93/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/KeSj3DdQAC+5QkVFgEd0U/REDACTED/dvz9CcUy2kHUOhKO+sky9UNFk566kCsBuban/vDqFq/REDACTED/EkBgv20byOaE4TqyhUAzp/dDPXVBRFuQPYD7hZhQnWm4J4/REDACTED/5GKOLcbDAVHY7d50/REDACTED/783bRL3+m0wnd4A7ENCn6nGQF7/t89Ve/4qd/REDACTED//pD//oL/+Vb+XGL//yG1760i/d+vbP/REDACTED/5XcE48vuu/REDACTED/REDACTED/REDACTED/N+kk+LK1Qz2aN0QP/REDACTED/REDACTED/zB/REDACTED/REDACTED/REDACTED/ffHZGmjghxXLXrVZlEBc0n4/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/cqJnIZb5lKsDo/hRwC/REDACTED/S++hX167OKrNDun5dmJPvv//Bxx9/fOtwKZvk0O4//N7voWRo/ZnPF/c/8CA/+22XDo8ORmBCed8HH/9TH/9xv/WmPfHS71Zu5/lyffXqDBL9l1//hr38W5/7OZ/9P/1PP/fAg2+/REDACTED/4Qj//ffMurji8d7+Yef/VXvfxf/tobP/TwW59+x/Oz4Wqn/REDACTED/REDACTED/REDACTED/B3ZragNKxtkiinR8suE+MfLkE/REDACTED/REDACTED/B9IzYOyqsaiUXTUa2cHTt3+SLa7/REDACTED/REDACTED/Mat/G6HpmrMbmN3F7FVmkyH06/GErQQjfoYVQ/REDACTED/fviI+SzPpxelhQjETqtkiKA/REDACTED/REDACTED/REDACTED/1ggEd27FIraz/IV0KC5drCY4+fnp4t/tb3fs9/+V+8ZPfw+977Pv4J6Pc+49M/HXTx9efKlat8wKWLhx//orv8J8LD/REDACTED/yhaPD3YN/6Ad/4G9+z/ey3fHypbuSqzv80GezD/rF5gAAEABJREFU04cffc9XvfwV3/Vdr/yLX/aN99///mfd/REDACTED/yv//W//bEf/cHdK/7Tf/yPXvHVX88mwsvHzyz9WS3OZO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/s/FChFAm7WY/REDACTED/REDACTED/REDACTED/qvanao9vb3p/2rulvFz61tTa/v503vZk/REDACTED/REDACTED/n2fZaS0yssBleuLe6667n/6v/6h5/x6X9m75Fv+c9v5S2L0PVp+/REDACTED/7Y2veMVX7B72qm975Sd+wp/68pe9gqXpnXc+h3ura9cPPfr+ZjD/REDACTED/LMZ96z9e0Xf/Gf55t/82//REDACTED/REDACTED/Xx8E2bQCexutZSR/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/dXVvdDWQro6vVG07nupQ6lpYZztADvrcfY/GHEv79+/REDACTED/+3/N4GCjrK+9nSSe3FGj3+B947Q/x2Q6mo7Oz5a/8yq9+yqd+8u4xr33t973mNd/5x+9+9Gm3Hb73/Y990Re95Ntf/W35GbeOBws0i6Kr15dB+OpZPsXv/O6/cfc9d1GeBv3z/+K/+IUHHnzwg++/REDACTED/ix3906xj+vOpV3/o7v/sfHnrkbU972keFYkDpbPxTzvHefsv5vTuFiY/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//AOWJm/faL+dF3C0tPP1TAfc0z+V/REDACTED/EBi+VmsZi3OqBZPk+l2G/REDACTED/REDACTED/REDACTED/REDACTED/ciyTEItRG985Nadx/REDACTED/REDACTED/REDACTED/REDACTED/sX0AABAASURBVNvf/g6ezZ/7uZ+9e87/4cd/REDACTED/a/LcXZ+xLkyNyMoEK0SKqlbiDyGvyquJhCqKcqh/REDACTED/REDACTED/REDACTED/2x2hP9Wnk/bW/REDACTED/REDACTED/REDACTED/i2/REDACTED/REDACTED/REDACTED/REDACTED/IdVdxLgc0gbQhlvQ/lPGn/ekDmVkzV5CqG2Hytj/jDouArvvKrWWq+8PlPZ9vg5ePDv/eTf/813/6qvWTRw+Hwkz7xE+jWPmZavefOCw9/+PSb//IrX/ziT9+NSb75s4VAqWdkPec47bc7n/6CayePfv03fvN97/5jyXbpf775m77xZ3/REDACTED/REDACTED/REDACTED/jnPed5z2lHrU1tbX5X3ibbzFO/REDACTED/REDACTED/FaolvWVK1anDmOxkOxhIQzn/REDACTED/REDACTED//REDACTED/tFOk/REDACTED/VBAsh5Mxh211TwlOZibRlv8owN/ht7hxTd3N/f/Aonp3zmJzspS3nJyp3WCx2O3dVXTeedz/REDACTED/07P/G7v/f7z7339tl8M5uv73z6xSvXZ//l/+9LfuLHf+SpnRNbY4FerK9em+eJfe9dF95+3+ozP/vzf/qn/u6lS8e3dM7ZXGifZ/REDACTED/47v/O6veNmX7575b/yN7/qmv/TKhz/REDACTED/REDACTED/REDACTED/ZrUOXc0SViyeYlHUrQybjTYsKfOmHxH/REDACTED/REDACTED/REDACTED/h4qEHjQiH82w+20iyShfUwCfuT6nEK/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/i5ct8lVv9/NF/fss3fMNfuu+97z2+ePDMuy7ldz1fXH7729/xW7/15r/5N77LSmue//nxn/REDACTED/f4N/+lV/7G//REDACTED//87/w2h/4PkXd25+3vvVtf/d//KnbLj/z6PA28vxbK8/j9hUoORaEnEwhydm/REDACTED/3BOClNhsNq5daB8Gb3OL50tb+o60/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Smq5uBrXFZ7VferdR9QuMZEg8raEFdsf/REDACTED/pECQCBt/REDACTED/REDACTED/REDACTED/vv8yU/REDACTED/REDACTED/wfqHUvUxx9//L73ve///rf/zz/8R///69dPSBgEm4/5qDsScvD06s+65/LV6/Mf/bGf+IV/9s//2S/840/71E/Ze04WWX/lW171ute9/ku+5L/a/fbsbIbX4JQzpDoGPeNph1euLR574uzPfd4X/bk/9zk/9ZN/97nPefYN7vzatet8Gz/8Iz82HT/9hR/REDACTED/1og988A9e+a2v/sV//k93j//r3/kdDIAff/REDACTED/REDACTED/h0tO8NOCk4L54Nz6hH1wXk/erVlUzLaqLaswuIC3b+lKVfpvvqzGcbg/FIAzyZ/REDACTED/xrBbHynxb3aRBo3KDb9TaE/REDACTED/3GSBwMGXW3txVIvUUJIigxFfI8t3YDca/REDACTED/REDACTED/hcnh0yqtPO1pF7Dq7dpYGm/REDACTED/REDACTED/REDACTED/2WrHBjGdSgNdFJNW/cUqmiwUKlGlld9c22dxaZsRZH/bZGOR7FU6w0fQdoqUW20P4/REDACTED/pvrY9V8kfzs+YfE3KiuN57bS93/REDACTED/REDACTED/9ve9B1/317/REDACTED/SU/REDACTED/+4j/7oj3rWs5556dKlk5OTxx97/N/91pt++82/REDACTED/8hD918Zg/F1nMPvHElYcfeeSBBx5gR/Q73vFOHHbvvZ/REDACTED/REDACTED/77/H9d37XD3atK1NVP+f1EfGJrl/REDACTED/REDACTED/REDACTED/REDACTED/Vbdpph1BW/REDACTED/REDACTED/REDACTED/EmiL9zPDzQ2sLG78/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/v/Eb+0/REDACTED/8Djz/0qGBsdti+8Y2/wf/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/02A6r9dt/V/REDACTED/REDACTED/Gt2oc7ms/REDACTED/REDACTED/ushCiDMLp+Or/REDACTED/REDACTED/REDACTED/REDACTED/R0eXbr/REDACTED/7B7/REDACTED/CBNks4Ir2Ti91L/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1CtKX7+n/xJi4D9q3/REDACTED/q/REDACTED/REDACTED/dL2Jck0Uy0FF0FDQPOGqH/w9/uTf+14MgNe85m/REDACTED/REDACTED/REDACTED/REDACTED/XYa8r+O9V/REDACTED/REDACTED/REDACTED/naLzulqhF+9uw0w7n7D//REDACTED/JAHR44YPZ/REDACTED/BOfoJ8TOnovGwUMO/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/BSd41s4t66wt3oAut/REDACTED/REDACTED/ODxQ+Zw2MDKXz08iDOjXCwC/R+fn0d/3T88oBA44oq//nq4CJ4QUeyREqdTlEQ6hRDaxvD/REDACTED/REDACTED/REDACTED/uMA3l66yfN9nGuag/REDACTED/REDACTED/REDACTED/QWsbHktevkSmSQ7bmvshw3NHqsfexi5So/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5f/REDACTED/8/GjT4CwXyUx+Y/40iikUdTE6J41BeFiYbiKik9YvwyJTdg/JbOxuadQuFBZrYRBxh+S8xmhBe7oZx4c/REDACTED/ah+7y9nz5b7W/REDACTED/REDACTED/pkX/REDACTED/REDACTED/MysPPbbL//4W/REDACTED/zValIJlHIsxYj1d40ZsvR8WRH3sxa8prT/UKgK/FbGn/pW2pRVB/mt+G2rP8qtSr47e4zr/yZ/4c1KQffvg+poiX/hu+X7mI1/REDACTED/W/REDACTED/kacrwSHyHDlSLky93cbexVd/REDACTED/REDACTED/REDACTED/iFLOiLyPfeczJMlQ1WL1+03C/REDACTED/REDACTED/m6juc/dzgeYK/REDACTED/ipo/e8f3o0/J4S+STtHtd9xTa/02wf8PiNayjNkZB+OZr/a/R0iwKN/GlY1z+C97DHXmtcL9lxfLzVsmz/2cGWfowySW3dDmrLknobpylMQ/SKnYI5wdwDtjDvsYIiuS9nMZWCqI3PLSSivf/naEZE3VfwX8OObtvrNW/3ENoHDm1t53p++uP/JMC/REDACTED/88a/qCaCS6TJh14/e/REDACTED/kwWfLyETEvmGxUJ8JfvfgQ/REDACTED/o3nWLUP8MYrw/TQ2Yk52MuYBPj5ULsH4h2y8X2Xd3u/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bbG8e1zI6f2sdIW/fZda/REDACTED/HwDCr57/z7EgEuF4dX8+uuve5IwDFHx/ou78fP4HELgAAAQAElEQVQocu63GEh1fHd/REDACTED/ug1hO/vT8G1MCDfQ/REDACTED/REDACTED/dEY/XayPns4ihymMdJW7h+I/REDACTED/0LfYhPNb95ek+Z//REDACTED/REDACTED/REDACTED/nv2jeeW28sK3+Aptrc2T/REDACTED/krs2Pr476hnhG/REDACTED/D6RgtFk/REDACTED/3QBumh/iR9GjRH46piNC3Co/REDACTED/REDACTED/REDACTED/REDACTED/5YIfj3+b66/su7RCjJrJ6kzMwQl/REDACTED/REDACTED/I97Z6fz9slGQ5nrxuGLQ3nsdNGn3Z58fP/REDACTED/I2tiv1w9ff/REDACTED/REDACTED/REDACTED/REDACTED/mhX/REDACTED/Ch+9NYd9m8dKHf3NLc/8xa//REDACTED/REDACTED/REDACTED/vaZrNRlFRq9cPZSSrebXx1lV7717DoesW/REDACTED/Xc/REDACTED/fcY5n963w/FZd5o9kkjNlcbdF/REDACTED/yZ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bvEaz++1Zt3qVCueXXHugQV6o/wMy/HC/Jw8c/ntlLS32284rrfbw3F7cTy3L/TSt7YvmZ/1k/REDACTED/REDACTED/uD+hnMC98yy7j+7pycsX3b87u7Xzuo/REDACTED/REDACTED//REDACTED/dT8ut1e5emrh+/REDACTED/UYwrJAu8kazZy6G68vFl9lIFcuD/b5Lb1+3v6dvegZ1dsjvPGbvaeyCGIpRyrX/REDACTED/4+376p7/66ovx1U/91G///REDACTED/xdKSuJpROesz+9e/PSFDONzIWzmTLZ/H1kUbebzwRP3Ej/8oWKB/REDACTED/REDACTED/SoHlx3+S/nGOagYf2DqDvwHJz/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/3aoEl4o3VNe30f5ItSMGH7Krz/+oJIextu8e/cwZsMQfZfueafDcRqVJM/v3r1TIZ39EKM/REDACTED/REDACTED/HiCu9Pp/REDACTED/j9cZDQTREcjV6ZqH5/bxyZ20CBcH+nXDgZdE2pAIjZK/o2EwfMb3z34bDzZqGQoDVQArBizTYS/REDACTED/PP/REDACTED/hw/0XnhG8ZarfIuemImI/d09ucmh7P6gsI6fN1Sjx/REDACTED/j2VWKl/REDACTED/3tf+urf8QB8G/7rb/p//REDACTED/REDACTED/REDACTED/VTuMvf+bm/9/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//V4zKPS/5Tl8vW8dvblYS2m32tlnptX1NJf2Nfj/REDACTED/REDACTED/REDACTED/kdLf5fZ8uMcMD2n+8DifzxcGqz/REDACTED/REDACTED//u+/REDACTED/bG8dzvc9/REDACTED/REDACTED/8k//Y//Y7xsP+P5L/REDACTED/h8Mo7vrXP9tRvOIfDWtmPrx/REDACTED/wt//i9+/5d/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/OO6qUhj5uOHHPRRR2QehOlqg54hsJlMMkl+zz/REDACTED/REDACTED/fnkPhQyVXBdUNRuHrs7/REDACTED/e3Z2dCMox2Nkx8ABi7v59//REDACTED/OJ3PYVDrHlst4jWOngYI7Ofz/REDACTED/REDACTED/nWaq9Pw/REDACTED/REDACTED/RXsx6eK1MeX6/FtOb69cbzUNN1kecdlP4/REDACTED/REDACTED/REDACTED/To4IH+Hs/8ev//J/REDACTED/7Q+35+A6qhX4xXNS4RCjc86r/REDACTED/REDACTED/REDACTED/93/yP/Ef/b2/93eNn/4f/09/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/HeghCzMWu3GEKAQunPvuPh/REDACTED/xZhAfq/REDACTED/REDACTED/REDACTED/cn55RCfzQ/5/REDACTED/yGr+eYBu2p/HUA16aU22Nqz+BHW3cHNktp/Pdu3cPd/REDACTED/ujEZbe///xtLkivHafrRY4587oclx9+/DtfPfw6TPmgGGsZ/REDACTED/I//nP/atovN/ze3/XT/++3/OX/REDACTED/REDACTED/3lTqFaqM48Xzm/REDACTED/ZqcIrR4a5k/nC9RTaQtoSlMsmmIixi5IWOV10/AWXN2nP77ft8/CvQ7Pn/hL/REDACTED/REDACTED/GFHbIHM5FlljewVWdyL/qXzWGJrvlaFB9YomjUi2/RrWNx2gP9wlUjkqK7xiI9Kym/REDACTED/FA6DHTH/ycObLvl8gNENua5ja1A/REDACTED/REDACTED/NRe6LtNa0+FnHQ7qQdDz902eEJHnBd/F6nfWsX/7mj3/F4IGrzUouGdTx4//REDACTED/EnZK7/Vc0/D89FV7fphL5q7HVX9lvp3Xt53/REDACTED/jum9kiLT+C7/REDACTED/MQapEef0f/vCX/rn/1n/vH//HPQr63/F7f8uf+bN/DlJCpq40V0KZcF1cIvuDDd+v16cJn/REDACTED/REDACTED/qoNyvLuAL5Sgqy3/17fmtQQMuf//N/8W//REDACTED/REDACTED/G10nvJ3Bu0W5Qkw/p1/REDACTED/amfxOhRlJWSXF9yh/REDACTED/UBBYiGpMXuCvl/vRBP7My76ktiDlRWHei8liTK/rWO1TtJh9Spl27GaSeb/9BbY97rvjTebMaIf9+SRv7b/YHgX0d/REDACTED/REDACTED/e7OI1e8LJDY+/HNuwf3qYZ1sAWHut/REDACTED/E3SBWdL9r+H5P45aBxuXkuRA+Lp/REDACTED/REDACTED/4OyxsIEkJkw+CqDDd7fch/5xmwXMB+dbcHpV9eDRS5CRqR4/7r29HY79/92OgUSQq4NMwy4UwzXZHyU8jQkSChFhk/c1zNTTzRzu/uf6yRSRWgYbo/9W0bGr/REDACTED/TVX724uPE3Rw1ohf/L82rurs+/REDACTED/pXfva/+l/5L4zd/8C//9/34QfXP/m//REDACTED/ezkz32IxDMHulhq/QlgqIn7g95U3OUsm0594SGD5k6/REDACTED/PM3W47w/+Ad//3/+P/fPYCj9C//Cn/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1Pa1x8HxHuOhIuhEOzDafr+/REDACTED/n/EefhjPQ+/REDACTED/Tw4AB73OJyBYGzDD/REDACTED/REDACTED/3KO8IjY5Q56sFS/REDACTED/REDACTED/REDACTED/Ud1v1zHV7e5zvJ3O+/0r37cW+fMO+vNjHvyeQHvtfP/78lx4FHWXtOmTMEhIWLWMM/stFRaB50d9OPTe+jv6Go0E/Pv7yu3c/REDACTED/REDACTED/tzNGQT0xPSqwWqKJOmpuQD4a/96z/zL/7xP/Uf+4//gXHaH/4j/5mf+Zmf+4t/REDACTED/+vf+4f/yfxaT53/6P/9TP/OzP3O6C/ZmrXdBshtV53q2JosBD33XM8+5V/REDACTED/REDACTED/REDACTED/REDACTED/2UYcfRCy1kemXpsL87/REDACTED/rwxa+TGz3oZtumJTW0pGX/5kz5/REDACTED/rMQrNOfYwJq71//REDACTED/jhs/uq/REDACTED/REDACTED/REDACTED/REDACTED/nlcJ1++HTo1jUriBejNNr6j/zh//RP/ZZ/aJzz9YcP/8N//l/66//REDACTED/8pMN/REDACTED/REDACTED/8nb/jP/XP/FPv378fp/ytv/13/jv/3f9BGW46Sxzlfnkm1/REDACTED/REDACTED/REDACTED/US0UOeFBXJWaefxB/Jquisypkrx3vi6rUP6VaYRsURLYofy/REDACTED/REDACTED/REDACTED/O78LTmJHocMlO4A5gKgbMu/uh2AZp40L371/N64gEYmkJ5e54/REDACTED/+wGHU9Vp10Sy63Q2/REDACTED/cgm9sINfW/REDACTED/EYV8mV7CI5LHb/XWr326rte93/nj5pR/REDACTED/+Xkhs944yV7dr/REDACTED/eNl86xZGvkjuQz6+0zH4+H2JH/7f/mL/z3/9h/86uvvCbwP/Ef+v3/7T/6z/+v/sT/jtdpL96rrc8jnvnULk2eWvsoHgjticH5/REDACTED/+Ad+/3/pv0jf7w9++PX/+H/y3/jyix+V0vwTD1X/REDACTED/REDACTED/REDACTED/L1B4G0ePKAdwIxhsodni4J/REDACTED/REDACTED/REDACTED/dZbSYJeeKZDaSz8bVhFNtoTYH/REDACTED/REDACTED/vopKW+0sO+wlYOA/v/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/sgnxnSfkYasLgNGjz/PbbF+/+pfvfsOXD9/REDACTED/70V8/REDACTED/REDACTED//f9dO/+4/+0T8CDCxBEP3H//if/kt/8a9UB/REDACTED/REDACTED/REDACTED/ocyt0BMA7YY08QnTs/Dv/0d/9H/mn/8l/77/n343OHej3v/Zf/+f+r3/REDACTED/REDACTED/REDACTED/ewkeSaOJRDoGeTyBwNK/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/SGqTMeD/REDACTED/EhB4JnAl/REDACTED/REDACTED/l+MpFub+WzLhux+fuG9V62+OyxvH+Y+Tnn/0i9/sVFgS7aPC2r/RiRkg16lPEa0ytAb7/DbaEzGoYCkb7v/7u3cUoOuSxkVlQWC2Hrl9Y5OjVLVcIj/REDACTED/6A/9h3/Lb/mN1WL/5r/5N/7K/+2v/fW//jf+7t/REDACTED/vULAsUNWrFfObAOAQ/O/REDACTED/HXf+93/Pbf8rt/zz/y237rb64+/Zt/8+f++L/4v/xbf/vvtRejBe+Lpwo/REDACTED/slW6j+zE/REDACTED/REDACTED/REDACTED/REDACTED/sQFz/REDACTED/sfwqrvoVtwwP8ac2tZSoJZW/REDACTED/REDACTED/9MfnRzhUg/2yD+h6//4OlXV85Ld2fb4+BevV/f0DwnRB/REDACTED/REDACTED/REDACTED/jlW17cb3v8le1X73/DF/REDACTED/Md/REDACTED/ljdMkNWN99Yl00aA/92E0/5raYu6HoLSUuus5UitR/FbX3ypEDQ78s//sHwIn1j/4/Nvv8z/7l/7UH/tj/REDACTED/HaepTgjKl+0sUxxrSGf+oIjcTEo7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5FF/REDACTED/nAev/F9/RbBEC2lX30iIy/zfYliv0O22qtV/REDACTED/REDACTED/yiD/cIe3a/JXyVV6/W+9GTfiOVt6VjIWoDjaf1AGxE/yq4CUEa0ZzA+d3D/REDACTED/REDACTED/QpPz8PosDvptDf6yfGv/REDACTED/9NC40cLVifu/REDACTED/noQKY8mb17eP9w/REDACTED/fJGcV2+stuvXwGQ+uKI3X6lr5/REDACTED/d/5+/6bf/0P/VP/IF/8j8o/+Dzb5fPv/wv/+//F3/iT//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/vTIPDZ+ymCF73JFpXtG/REDACTED/REDACTED/REDACTED/REDACTED/hhao/REDACTED/xiP38w10H+dvEGY/UXY8AtLv3+3cPv+b2/6x/+h3/7T/3m3/iT3/uxd+/eyT/4/P/P58OHj7/4C7/0N//Wz/0///r/6y//5f/Hx8dHDCnP0ZEZSo0xkEHaMVJo0Qr2/REDACTED/C//REDACTED//iFImHKji025QUBOy1UoEhEim9m/4oGp0QrRznEdTtae+m3JJaxgdF/REDACTED/REDACTED/Yzy6Z+zZ1n7nfyBA490OChpmM1QxCNC/7Ad2/REDACTED/vHt3CuIl1A4fk/REDACTED/cn511Cgh8/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0cPmKHKsFziFlx9Be8/REDACTED/6/9az/7r/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/IhQ2j9UYKEEhJwgd21LLd/REDACTED/REDACTED/REDACTED/Z6SsP8w4Hcc7+0ORy3kt9vH2/Lcey3N44fr6OlmB7UYM0ZBeujyIy/aF4/REDACTED/DATrvs1IsBnz8jmYh+/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/SUBKpJjmUODVv/tblfzQ0UlcnDSRsmDK7I/REDACTED/REDACTED/REDACTED/d1vaTe1/REDACTED/REDACTED/8St4SaFxZdcae9Qk2stOP/REDACTED/REDACTED/69wWnz72firsp1A/Iu7H78//REDACTED/NYJNWtVO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/BtzTOf/cOwczjVs09qHt/REDACTED/REDACTED/va6h32mD7XJIu5Oj8HD/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/jQM/REDACTED/rHNY2vID3iaaEinBeNa8GR/CAs/REDACTED/REDACTED/REDACTED/REDACTED/hmcnjmurEZnZy6HnINpjD/HZdjjUMrMWHgoSJG/REDACTED/REDACTED/REDACTED/piX1/REDACTED/REDACTED/0lpEcbmuEBXMA1HHZiwdiP15DT/REDACTED/REDACTED/REDACTED/tgFCs16IXhzLCASa4/qdSaTS2SM/A7HC8t6Nvu/+DD3/REDACTED/HMHz/7qscUFZrYCjhU/REDACTED/REDACTED/REDACTED/REDACTED/Zh8sQGhHce6jNWyhbZ7hAti2/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/jyj7XV1+0bx8u7Ql2ZQ59T5dTOZb/z4ORYscY7R/REDACTED/REDACTED/REDACTED/REDACTED/lHv7j/REDACTED/QpcCXPSjkLzYl++/REDACTED/REDACTED/sCem5H/mEs8Qmp9mMLNmDGWU8aucUkxBq/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/Z/t4/REDACTED/REDACTED/1mfVEF756M2/REDACTED/RxVEqwWUlDPBuldO7/REDACTED/REDACTED/REDACTED/5gfsSkU/REDACTED/REDACTED/ZEeQxtXjc+zh/REDACTED/REDACTED/8/REDACTED/REDACTED/REDACTED/REDACTED/dT7KuoYe19PcPe4foMe33ccTLOv4p/REDACTED/REDACTED/M/REDACTED/DdOwRkoraI1EZF3Add5F6o/qpCUAcDFFJinBntV/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/yCOEYU5GOe/REDACTED/h9oXghE4SV2lL5oB7bq/REDACTED/Hru/REDACTED/REDACTED/REDACTED/T4//j2J778HVBRqOkhgFAK9mN/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/zcEvgJNfzUbaJ/REDACTED/REDACTED/jgYKih3RVBjzEzzzCH/NC6ATP3+asG63XJQ1/REDACTED/REDACTED/zQm/Rw8i/REDACTED/bg2nbX3Afbh0t2XP3h/REDACTED/94B+7hmLTb5mTPTn/Vx/eeQhQm8zEprteLuSP37v7O/REDACTED/REDACTED/REDACTED/2UNUJe6OULcpZFuV+/qtH5BoTTUtZV05eo9S46r2CH62S/REDACTED/Wt6Mw4H31UP/REDACTED/REDACTED/REDACTED/REDACTED/jgmG0Qj0HYbbPp2x6wKyCr/REDACTED/9s47rt/vvklP7ll9x72Tz21DJ2+F3k7inpu/6Hf8Jt+8MNf/vqHX+f5CQBynX/lbq/REDACTED/REDACTED/REDACTED/HQx92OA8Xqs2k7UHPjN5e/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/hV/REDACTED/REDACTED/j8TTLUU5bPicBebUqflOW9aW1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/9U6kmKlNNacnFB/xT3l1NIvtxjcfHp1yN+du1qbH/REDACTED/REDACTED/REDACTED/HZ2afGgPcA3QhAcJ/xcO06lvTgkLu7cbU79/REDACTED/REDACTED/k2RN8UhWlEIkxJD5WW4s39N4/retw/LcNmUqGQV48/Xr7/E1/REDACTED/REDACTED/4KP4Fv1JlPY7VNxiAXxDrEWGf/REDACTED/REDACTED/VvtGb3P/uWzgeeWuZrpqyCmy/REDACTED/t6p/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/D9ppWR850/REDACTED/4bsV9N3jwE/REDACTED/REDACTED/M/Rzqizany/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/FbNy40PrlBl+feR+F/REDACTED/REDACTED/8/REDACTED/REDACTED/REDACTED/FWnqJfU0Fw+e1kV3K2zzon9dO3I/o0Sj8r6wC6XFRxR4H8OmjH/REDACTED/REDACTED/REDACTED/REDACTED/DdHQ/REDACTED/yKEN/2Hd/REDACTED/Z8nmn7cg6Gl/LZUpHMpUgXTVmO90IbtjlJkjLKj0/REDACTED/REDACTED/icN/ZgCFElpuyrZCKgrZSrRbGc+65LxyGUu2sE+2u/REDACTED/GNl9CrLJ/REDACTED/REDACTED/2gZro/REDACTED/NHko1DEovmo8D12CHKUtg/REDACTED/motBXQd/REDACTED/REDACTED/REDACTED/P4z29Pu3wd57BgSwRMtc8ITfA/REDACTED/REDACTED/kgKlrIs4pWf/fyCKzN2Y0BLHwRUsOu1y9fnn/REDACTED/REDACTED/tC8XGVUiNglf5M/REDACTED/8tofslNwrk1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/yh9bVswXr5rbt3GlZIe8uu+fdV/REDACTED/REDACTED/REDACTED/REDACTED/DExSWC6S79+unnv3j3vc0QYSqsQxc/aqUNx3IB00IqWnmF6aKbVvktNFl1P/REDACTED/IzLZqJMm8pbpAt5oMefj/REDACTED/REDACTED/1HHlsP02cjzst5Eva5qZDU/aRmB6Zem3e1nD21L/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/RsW6F/REDACTED/REDACTED/REDACTED/ttwIw+BfkWENrXQzEDNJTOCkM8R/REDACTED/Rsegu2kZBmrCHh/REDACTED/REDACTED/REDACTED/Wo9MNvtVhMO+3cBZVfbB/OX92fvujE911y/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5u6/2+SJNetBFGAHpnVfaWRNNI8s3n/vO//REDACTED/GZ8/swu/REDACTED//zyZe0DfOpWvqolL5CRuu1yB355/REDACTED/REDACTED/m99oRQt/+bLqN4/RHl0WtEoB/J6KbzLYO8Of/REDACTED/REDACTED/n4DUvr385NKQ7l2v0Qksv/REDACTED/REDACTED/REDACTED/tfYfwoOe9bdu4S9zvmSmOWIegjcZV/ygqdzv324pryACr2saqT6C0dQatxL2oqhq9/REDACTED/fSgXAmgzoum3bf/REDACTED/REDACTED/REDACTED/A/REDACTED/REDACTED/PamFv+HYHG8bUftdn9Ylw36/REDACTED/REDACTED/l8jkVmW9fv95TxV2xrLkD2amsfnldW/6szMzlE17pw1lO+VQ/H6du/REDACTED/REDACTED/REDACTED/d1v648gGnvvZt/svr+C9QBUPVQ9YcUYHMzR/REDACTED/REDACTED/0vniqE/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/DpYJZRSDSUgWJplRpemDslVl6o7vD/NE10S3LAqhDQg/REDACTED/REDACTED/K3j9px0pAj/VdD87gviilBNFvB1QGagnLb8Hw/ZjrjLEWUA40wfhwDzduSv/REDACTED/REDACTED/REDACTED/Q24S/REDACTED/REDACTED/w0//REDACTED/aZ7J6P/iVKh+RS7fBoESFnyrf3JI/REDACTED/REDACTED/u3Zf4/REDACTED/wWnkaBKs7lROhqiaUoUbozu0UXh/REDACTED/OjDTZHn1IjcyyTH5JF+2onDS8x+OPb/REDACTED/REDACTED/REDACTED/REDACTED/hGNsT3kSon/O0fbx/JU+fE/3/REDACTED/REDACTED/WfJ1fyHrLt5Q9q+rVCYDshpdarj+/n9q53dL/REDACTED/uDYWflkawfDn+Gfwx/REDACTED/xYbFqOQJcwo1o9LpG/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/svbP/REDACTED/jZ/REDACTED/oRwCtutM4MO3/7r8GeUZU+r5cLj/+/6PA/V7zzi8/REDACTED/REDACTED/Yuen/REDACTED/PIHRQyqnkth8yIXRvqQo17oFCpZ4XQtU/P+1vWdE6mGQmP8vYps2+8cnHO1YdV/uqBRbpeNXv63/+///0cmX/8x390Qi3aY8mXk39KloTq+j0mJd5oC6/REDACTED/m0FTJ9rOcuL/REDACTED/uS86G3+2y3ONfAHAzxZ/REDACTED/REDACTED/likCgE2iW/REDACTED/Nwmb5S2jP/REDACTED/r1b8SSrCUivNdNa6d/REDACTED/GbaHzZtHQy3HujDr0i5h2i/REDACTED/B3f8IKCP6qjvnhiEd/1GE//REDACTED/QA86L31fWbu7H+3I7/REDACTED/REDACTED/zDSY2glX9veXUzf/REDACTED/tyd2c08lz7+yaP6/q66TJdHHUuD/REDACTED/dgyvpA0lAHS0PYuBS/REDACTED/jDeUQ5k2Td0oMIGXPsDdD/REDACTED/y9vf/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/TN7fzZa/REDACTED/REDACTED/ETJR1BMa+VVs49/REDACTED/jHS6Rk006cGOqCA/dM//tN6kQw8fn1d0cfJWKnzsd5eSqq1a/REDACTED/REDACTED/REDACTED/Zq/mf16/REDACTED/REDACTED/REDACTED/REDACTED/f/OPFOHMSaCnIemck0fv7DTz//xeu//vMfXUyIzCb2V/ELG3OVp1xv+Hib/REDACTED/Vv1IW/O4RyjN/REDACTED/REDACTED/LbNU6bO2YxG/REDACTED/5TOHD/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/eKl7H9T9ahJtt5b43h6thzxfCSdOPb65f/REDACTED/R0KfUABSbvGb1/REDACTED/FUw5FqrBsxNmEeguuoqyZ1NCK/REDACTED/Qmq33JXNG4leam/REDACTED/REDACTED/REDACTED/REDACTED/3tgd8u5jxEkweeyViSipYSzY1//eP/REDACTED/REDACTED/REDACTED/KPppTRgExCLzYKZtnsFjIb/REDACTED/vnOwj9vf1SM/REDACTED/REDACTED/VO/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/eNw0uwsPtA0WlwSP/bnWXmLZYHFN/REDACTED/REDACTED/OacfVkY1tdVkcU2KvGTCtCtDH13b1XnfS/REDACTED/REDACTED/+2rjm+vv/x67d/REDACTED/W4xyMvc7jAF5pvRxgoDmJNLf6ceWFRF/REDACTED/Wn+xFk9FgwJdeuq820Xp/4p11eZ+fVdfsnmWvWMGg//obztnHFT59rPzofWi8f9cpfO/REDACTED/REDACTED/REDACTED/o+j1wON0tFcUDDiXtw3F6OI7nf/f3xfo7s6Y4+HiHww21+naEdWY7r5XX5m1/REDACTED/y5aZz/REDACTED/REDACTED/0YW+Wtq6KUVRrqmBjZqYJr/iC/72b/7r//REDACTED/+VT9uFX9hKmp22fD9KB0/REDACTED/REDACTED/qgRXGHYZo3NlQsUxvClp6ZonY6Aul5/5Krg2z/REDACTED/XMrINWkZp8QB+Yky9/REDACTED/REDACTED/REDACTED/SOM/REDACTED/M/REDACTED/REDACTED/REDACTED//2v3758vov//REDACTED/wpGSunp19hYfF2o5Nuewbs/l/SPu3H6c9F6O3a/v5/REDACTED/gwEmwjaSe1xbSK/REDACTED/REDACTED/rdqEM019Kx/3OCB/REDACTED/js3vLWDAVboTy+mNlXszDH3f3lwJ/REDACTED/REDACTED//ytdh6kF2H0IfgBY/k88CBEo+2c5S2ZH9UnpVDJc/wtsWON8tQW0VNPlHCSzkf+/mpEj4dM//4ty/REDACTED/REDACTED/GJ56rgX88/REDACTED/REDACTED/REDACTED/REDACTED/8h//REDACTED/REDACTED/REDACTED/tvf/tP//OcT3MJ9kUftZtRKJ+lJxBCEn/REDACTED/cPb8bca9tMLO3X21EStbHKjlt+R3u/58d2bM8FVpzVngIRbO966Hf003rn+FS39S8//REDACTED/REDACTED/REDACTED/RWIV6bYVQhxC3lSVYD/REDACTED/2HbfnBN/REDACTED/REDACTED/REDACTED/REDACTED/PzmVZaBYRm3dkQeUdHtplo/REDACTED/REDACTED/REDACTED/REDACTED/8ZbYvm/P957Y0XPZ/XJAs7/REDACTED/XK6hUFO45aKa9jbKjc1c9/REDACTED/ZDkDyzTdsbjSyFDkFfx8Q/REDACTED/REDACTED/x+yO0SwmVGNGcKZx2tQUpMSD7U/FShqc/REDACTED/REDACTED/mpV7e1fkiC9NqwOiRN+i/REDACTED/REDACTED/HEcaobMWqq0koJd/+Lf/REDACTED/lstgG05gRgEd0KyyKv+y7O/N+m8tvxZPVjhcnKMBZfNCndM/REDACTED/REDACTED/3t+NCOS5uM2iRX+zz+lbmw2t87/REDACTED/REDACTED/sVXj2eAVT11m/REDACTED/REDACTED/REDACTED/737YLnr/nHG/3oE5df4vk8hq2w0oyv/REDACTED/REDACTED/REDACTED/REDACTED/NIQUcfCC0GCpcXtKx/hq4/REDACTED/REDACTED/REDACTED/MfXv3+//7s1woQVSOzSZdoq/REDACTED/U+voYuYuu0JsuEJ2V4BXAwPbajtDtNaS/dERN/zQ/s7Hf9j+c44f77m9sF/G5zpW3zsWlPqkXY8qHTZsE3V9/REDACTED/REDACTED/REDACTED/fGLBEfkDCZLiCjJheRQdT/qZkyerN3Nw3628z2Jig2TcvH0BJw0qF/REDACTED/c4mdSTzNnO1cYyFbBzOlVj8n1m5HlnmYDPlN/SAZDMBBOb5zQw+H3nP3iDi61/dj6l2NVj/Ld/REDACTED/REDACTED/OtBAJ++3NN5rpm/27w/REDACTED/Ps7iCD9/REDACTED/37MrD8PQuRXfd+J43X1OY2j/apn6a/REDACTED/REDACTED/REDACTED/oHY3An1ODK3CzJoGJUMLvQ/REDACTED/REDACTED/0HJpwjQgxTYRYsG3iwFbxBoqe/11k+RNMYnIAtDZML/REDACTED/31jpvXvocavKDY937O+efebskwrOM/p3n613id/bHuC4/Ykv/3echNZ/v/REDACTED/KT0egPla8P+6pja79hE/REDACTED/ExTzeH+/jbu+Lp/REDACTED/REDACTED/vvkaWuR2PDIYa/REDACTED/REDACTED/PomasuuU9XVv5B+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/b/ErhYX90HoDPl/Y7087/nlG+9zz/cMRdEl0eqXlk/REDACTED/opOc/REDACTED/9rxpPm/HJrAWe7MFPXeOd/REDACTED/M9/+/REDACTED/REDACTED/REDACTED/zedn1sMuSpmX2x+z/eR4YPGmu/qsLG7UmAJ+/IX/REDACTED/kb8sBA3zpZzAp7fjky/me5PbEiVk7v2/REDACTED/REDACTED/dYEz+/HnIhw2MZD/uHWdaIjhUFsD/REDACTED/REDACTED/REDACTED/REDACTED/eq/REDACTED/REDACTED/REDACTED/ue//REDACTED/aF/REDACTED/REDACTED/kyTNy26WBvrif6V/D9uHevuO/83h5mV/5fBCzf/pj/3O6EPt68d907LX/q13zL3/REDACTED/MztlIY8ig+ljIB5n5q5Z/REDACTED/mqmx/REDACTED/NmCMdKISl/REDACTED/vh8Qfc6LDbl9e/SAyo1yKyiw0IxgcWtXmEtlC6KK/F2KNXDlo/REDACTED/REDACTED/fTy0w6+S+iJmAvVmo7g6vGaC9/REDACTED/REDACTED/RN7/BiQtEJ47l4O6Tq+Lev/REDACTED/REDACTED/h8ACsfr4/LX/cogxYpIMeWKWQqu+f2Ir8+8mr7E4/CvJ+3/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xOQv0bvuearfpF5ICeMR2H39dQQt/REDACTED/REDACTED/vRDBZtso8w2v5/REDACTED/YVhr8JaRBS65i+NDe/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/jyE8/REDACTED/tY0F4cEb4sH0oxLEQGprdSZBe/REDACTED/REDACTED/REDACTED/REDACTED/cLItUoiO3gm3iDngdm8ua/REDACTED/J7JqAX2Mg7q6lzc4Vp5ITvl9bUUD/REDACTED/REDACTED/66+qWaibs8I85Pz7vuZ60e42va/REDACTED/AdiqeS+6zeOD/REDACTED/REDACTED/REDACTED/ftZusFDCoNvkBW1Q/h3t+GE7fks7aUALwwl/tKMFLPqftgkFGn/REDACTED/REDACTED/FIiy/LYj5d2VbYqL/REDACTED/REDACTED/REDACTED/REDACTED/Or+9V008//REDACTED/REDACTED/ff/REDACTED/REDACTED/REDACTED/LqTwS9KZPKcJclk8BV5s4t2t7/2yp967VbVddab/ct//3u1B8X+9s33lmf8v8f+HxoiV/aP/Jx2Ka8et9CGtJ9LH960essQ1rXdu/REDACTED/REDACTED/REDACTED/dfyxYsuDccHuyoZtH++yr68U4IwTX/r7+vPwjgyvKGgVmo+MMD/REDACTED/kWARFLUZAlBK2hNvz9bLKlDWU1t/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//Evx/REDACTED/z38fpljJ8HE7ESa7oXxxBNco7x+emnn3/55Y/REDACTED/a1k/REDACTED/dxeXamSztRFWSLa1wdUpQqvz4FeVXyII/LvaLZc/az/37f/e9m8/zosNmfep85/c/REDACTED/REDACTED/WoB2It4FWdArnWxbXsnNzH4oyVV5T/REDACTED/REDACTED/REDACTED/nP/Ou/YnLiWbE/Eorw/5he1p84UlZPY/3x7/8zR/+SyQN9k11F6j5a4ml/6Cc9fAwS9+VJOGIKOPbGLn+9vb15eWn/REDACTED//REDACTED/REDACTED/KdQmDyfaTs0vpfpjHEMGVNPJ/REDACTED/v53m/REDACTED/REDACTED/REDACTED/jMjXTmdtuov8ruVkz26Wg/bpOxbG27vsTWfhKnf06b7/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/NbSBJeatPiQM/REDACTED/REDACTED/REDACTED/REDACTED/u/REDACTED/REDACTED/REDACTED/REDACTED/+RIl/M1JrOh1rhc3+ricmwpjF/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//FeOr/xmV1GX89/REDACTED/REDACTED/KBH9QwZPwEEx40Kj7EBKUeZ2o4ApVRfIFbZ00w0/Trwqs/REDACTED//KLYlxi1naPYBuoun8/P/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/sDwYzu5bB0ok30ykvZtyi5OQV/j2cvhele7hsqCEb7/03INPUK6EsXLQUjKE5P7+dr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/krInmWhc+tv5FnZ/rVyM+u9/2Ozvwx8e//nUGQoMR5dtEc/REDACTED/REDACTED/doF1Fn1/REDACTED/REDACTED/REDACTED/REDACTED/V5qr7rywwjW8ZrGqGghEzJn/REDACTED/REDACTED/REDACTED/REDACTED/Hq9JXqPHxg9gnX9o1K++nfffef7j/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/7Xe2SVffaf/G/mxtxuhh3f3+dkuR2Nq/Ms6/REDACTED/REDACTED/3DEb2dBCdfUOcMKzMqb2e1rKXG/TCOSV+1q6/6ynv54mVw/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/bJY865gly3/vTL9q9RI1EK2TZuTVkhCJW+tCW/V+U+IwCqHm6skt/REDACTED/REDACTED/REDACTED/qSRaZLRMbPZS0I+KmrSlsC7bNIEuK/hKPL7kvh3EhS/JyEMv0Cy/rcBZNVriri1xINOSHWBmrJ6e/4Ze3f/REDACTED/REDACTED/REDACTED//8HtKfa4zvtH91nfD4jl2Pl+lb7R9f7T3/5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/sU70qLVsze3j+NXMO+83H/REDACTED/GrM2+7wcratqw/REDACTED//wj7rBFaLR2Dy6hMgYnyjzSXB/REDACTED/d8+5t8/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/9l+3U1K2yW/+/MkyX/v8bmnn9/+e+3/lOOvdeHanWfP/O88EoBs7V/REDACTED/REDACTED/u4KkUe2nMAoSDQmj8ms/REDACTED/JRTli2532+9zBWqX47icqWjN33gU4jX/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Eeb+/3b0/SBAExlPJEiWhP7Jq4c/REDACTED/REDACTED/REDACTED/REDACTED/Yx5iP00n4yrH0pn/REDACTED/UhjZ9s/REDACTED/REDACTED/R40uhPBMPj5KMDMCIu+QhZS4f6/REDACTED/REDACTED/REDACTED/REDACTED/Oix5vb+P+Pr++/REDACTED/8A9II7+LbS1X5b/REDACTED/tAK+AnbfvQRn8+a2/yq6Qp7MDfaZtY/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/zq/nawhLpF2Etcfv3z5g7e/REDACTED/FXKuW/REDACTED/bLoNLyhQnnMSwJfHynraLZy7F/REDACTED/UJ/K+1X/CaSQ5f63c9n/REDACTED/REDACTED/Ey+2EF6ilGO/3X050kM4Mpp5Cydy1Rdt+tmVF/U7KjPV4svJDiHkev9z/REDACTED/REDACTED/REDACTED/SbsPMdqYHwyu2VNTCLtR67/iZ1+Y/ROv61GZPA/Ac7mAK62f2iPve1iJ2oDSuxt/7xtH9rNJcGS/REDACTED/uyDW+G1Initanmwx/REDACTED/AJ22PChd8Ptp3zn//6L/1yhJO89NrovrJa4btAaim9tM0MJto2O0PX/5mGeaMO0gztTCtzrPoah3nTm/REDACTED/hWw5wZ/REDACTED/REDACTED/REDACTED/REDACTED/2X9/REDACTED/REDACTED/6Xfn7Amf8zjtHS4ZP2f8rx9/SnVv2n7Q+40T6c/REDACTED/je7/e3zME8VD8BVr4VPrNqD5/O3yPLBC/REDACTED/REDACTED/REDACTED/REDACTED/H4w+t/zVWRywu12I/REDACTED/REDACTED/REDACTED/REDACTED/0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/vv3j2aOfv/REDACTED/Rfc09PF71aWN8qxzgMMQ/REDACTED/Xvd/REDACTED/REDACTED/REDACTED/REDACTED/H2NiEUJwi+z9Bdz86j1f0hnSX8/aBv/7a+Xjy2Yoeru0JC8iHXN/REDACTED/0/REDACTED/lUOQbElyuWZzo2wUg/REDACTED/h/REDACTED/+J21/Pu8X0fGrbW95MuhufD7vu4XSu9RaPbfFi/REDACTED/REDACTED/2QLMCiISdSKJ/mXEOPl67/REDACTED/REDACTED/IbkXkzradD5G4bfff2tt7bb/REDACTED/REDACTED/REDACTED/REDACTED/WeRY9Es9hRaWk2z9+/af3xy97/REDACTED/REDACTED/REDACTED/jSd3dcd7ON2pVmlaoXdKpnsY/REDACTED/rsQ17WdVrtN7fte+8PxCek9tX//8fKA+aH6K8hotl0HYlbr0b1jEGRfcsXf/QCXYmaJEOp8/REDACTED/GJWTs84zwdWR2cCov5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/4Crj2zAVlYO7qskp8781GV/AnZ8T44mpXq+Pty8t3Tz3oxHp/ZbOuvTPcM3oNnn/dIR98/MYoy1weKgA7tWT3EkohKTWsGhMito6k/REDACTED/REDACTED/REDACTED/bt5Ms9zq5vjjt395xJun88TS06jiT/REDACTED/REDACTED/pO1czezPc9t+pX2BK9AzLu2izU/b/ynH+ND+/REDACTED/REDACTED/d32VFUPA5h/REDACTED/REDACTED/RUtfPsMzQO/+/REDACTED/REDACTED/REDACTED/REDACTED/TqS8UHjHVQcdyW/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5vo+tQv+zB3mFN/5rW0x+Wrb3iY7/TCgH9ohbl7tTfL+3rZ9aF/REDACTED/q7/575aKEPhjlggeWRuQgIYZGhnYefosH/REDACTED/REDACTED/F7rcsRIXbFjJW3owrm/REDACTED/Px+fnbfvnGdcUVHa7DVLVb3Ol/REDACTED/REDACTED/REDACTED/K3j1yfmNgzTeAPfpv/r1Pla9jNzBmxm84NN5jczkIo/REDACTED//REDACTED/tW1CotixWpwZUevX6t/HVVLNhjTyRKkQ3kMH0fxVHGtXXmfn/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/rOOf/VXf/X6+voP//D3v+dbHIffdD7KhvtR7RRb/43neyp0//38b+tPXPWy6/HT8xfsp/OD/CF6j3Tbccv/suPt9NquNXA6LFeY7Xh9fUFgB6IsfNXBuoG639/REDACTED/vMdAooIefn/REDACTED/PJbL+YZCexSF2AuOubLrc39/REDACTED/REDACTED/eIBRwlfMQvnZ/5FZMp4sL7+7DAdn/REDACTED/Qv7/3KDR6edbkj33qJDW59vjYFGRhno/REDACTED/REDACTED/RphkR2W283l5+ckKcnVJsl+ux/VtX9Mm+63Nj+4Dd6/vSlRyQ19UB/ScobFt/REDACTED/veQ51nq0VpC/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Gy/REDACTED/REDACTED/REDACTED/REDACTED/PZWpm5rc4qx8qm4rtP0I5qcRvKj8a2vPJx/p491s2o8uvHqf+8X/REDACTED/REDACTED/REDACTED/HRQALxQCiAY/AXv8kJGa3BiCARa445LaXT1+g+y/REDACTED/REDACTED/khdOXN/pz1iCq6mOnyk2tfsBEsh/REDACTED/REDACTED//REDACTED/REDACTED/00/9rjbP1L+yOgeX/WrX/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/UX6G3InzmlUtk6c91QTq/REDACTED/r+Zclb9UGVQjdSqihAw6/REDACTED/u68D91XpeM1ZWVR/REDACTED/REDACTED/sw/c+45Af6adO/GYicbEHwnnDohK3gSA8d/REDACTED/qbpVjnmn7MMry8XS8vkf/REDACTED/UKkTl0rER/RhgKDI68C2LPhY7/REDACTED/REDACTED/REDACTED//REDACTED/0bnuVJSmau//REDACTED/BxllXmyufrFb0DB/REDACTED/REDACTED/REDACTED/REDACTED/D7+yCHjkecFjRrAOzGbtPPa6L/REDACTED/REDACTED/REDACTED/shFtkgyr4dkxuiuHFzsIh/UgZyosR8F2w8nJuphRZ/C0edI7WmRresRGZnP1qDE2/REDACTED/REDACTED/REDACTED/2w0bCj/f5A/REDACTED/REDACTED/4DD2BJm+K/AiO6ZckNNcFdWn3hC9GIKDh/msK6y42XYHywSQFjQv/REDACTED/REDACTED/REDACTED/8gi/YTvP+orWSr/NvHz/REDACTED/REDACTED/P52Hxqu3A/REDACTED/REDACTED/REDACTED/WS1qFGTIArtrlqxcpq1fnuqgOtXkHY/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/DebqcNK662uvyKcorkeCaBf/34l//REDACTED/KA35R5H/REDACTED/ARS7HLcdcdJxupSo0x/REDACTED/REDACTED//Lwxm+mVUhsY6fxt2/hOrFtNXDd/REDACTED/SMrJGrF3cvalIYndd/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/N5cPJFJKyQlwGbGScPFBviCHFVxw/Eec/r8g3M/RvU/2Flsn1P679JKY2t/D6ON327/p1y+fuODaMWlDyv/REDACTED/REDACTED/gK6MAV9/REDACTED/REDACTED/fl8+jI8fX/REDACTED/+VCEN0+tksLJu3XHEj/dPjSc2/REDACTED/REDACTED/3aEEIs5EzIk00w/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/vh+vKHf/7nP//REDACTED/8X1wg/c1P6x/oIGyq29Vs4Km8V5ST/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//2/REDACTED/REDACTED/D3o/2Qh/2QGeijhZtOFi/REDACTED/SiLn3K+r/REDACTED/Us624m8I0WOSTC7f/REDACTED/REDACTED/REDACTED/pc3ZfxnFQn89/REDACTED/REDACTED/REDACTED/WDGqpcQ8RmjyPMuXD/3+Fnc1KgDBOMPMqR1wi+/REDACTED/REDACTED/sA/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/WHkibz5/XTur1RJ8XJTr9b171eZTEy7L/REDACTED/BFr35ZmyyLzITIE5q/REDACTED/REDACTED/REDACTED/REDACTED/eCOFggqQ9+M6W0U+6WKffXlgUpc+avwh/+TiDIrsTjWdYUBXIvoksRasfsBDcyyh8MI/lOliFyQf03phrOAzOtzWK7/REDACTED/REDACTED/REDACTED/REDACTED/FdKxyOfqL/REDACTED/nxfKZFatlEYu2WIgxBzQk6wt/REDACTED/RnJmZ/3kFu7MbtENTFLCgy/0EnyXAIwQwTgKYEuDGMSNv/REDACTED/efIGp8vUcrIyWE3/UrlN6IcAAnPl2wEGHPwZoNkES3G/REDACTED/REDACTED/R2Z/REDACTED/98Q9/uFxf/vKXP319/SpJTQL9Q+Hr35t5SMk2y/leSrL6/l3/REDACTED/REDACTED/REDACTED/REDACTED//REDACTED/26V78nh0OkGSAHOl/REDACTED//PnLX/REDACTED//dd//emnn/6P//3/0EqsztRpZhV/S95xKR/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/0mrnYyjKxLru7W/REDACTED/H9def1/REDACTED/tslP4zCudvgPx3Qnl30p71/oM+OAziXbRaxLt/REDACTED/REDACTED/REDACTED/qWrMdQahogTGBO6/3d9Wb+uS+jvvNCob//REDACTED/REDACTED/lz//REDACTED/REDACTED/REDACTED/HaYuJ63Y/REDACTED/bf/+/9T17Xpx/2/uywM4kn8GvcBTbeEXi/rxuCIzsStPQek8OHXGd6/REDACTED/kwv/BBpwqaEa8rjyvIBk/REDACTED/G0y2BMaL7E3LAfre/zW8djUk/JsL9MeB7J2w//REDACTED/REDACTED/REDACTED/54xiUJZPvifmZjxUIL/REDACTED/REDACTED//kutInJW/uRjsVxbhtg4/REDACTED/REDACTED/REDACTED/REDACTED/kr3/98sunCVKq0shn4h/REDACTED/REDACTED/U/+4yV+D9JWS6N+p/X3laZ65b1X+b+b5Vf28Z+lvhPmrjsZ++V//t//r/uB/vm3/o/Kx4M1GIy6zXF3eAdqtnuLtMrLF/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/JKwrkWX28bkZWP1z/gpJjCn8GAVZI/omgrIdrCqJueYjhHZEyKrZWL0m/BJer7CX+5/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/2QmZ9ysiMulSu/REDACTED/ed+GxEaivX7GaehT5e36035+u/pjuVuDt7rmifx+/2DI3qgnzP899QL97883VVKtHjti+v1y/k+/7/REDACTED/REDACTED/gxV2zwVk1cJ3/Rakw/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/R8JgTa16rcNbJ6vlSPzGex/REDACTED/REDACTED/L8Gsr7vYShNsQSBQxr6QB+OE9h6hYy0n5l/SRYhlFX/fpAwfpfW6heR1zuh/36soVBJGFz/REDACTED/PbGwJblLGwpgBoxijNHOSKCdEG2/REDACTED/OYbXXymVkH4Qyswno+86QOGSGOyI/REDACTED/Tytt/cW42ibNdsa9/uDdWKhe/REDACTED/REDACTED/REDACTED/REDACTED/5Xzu5HemeeBg9O+HrU4HzuwJtunDXt6gvZct4q//REDACTED/aefXv5oHrfp2+vtl8i4N6VI/REDACTED/REDACTED/djeRR1FTuypHazPzr9USPIYS/REDACTED/REDACTED/lQQ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5TNYFdCRTTMQ4//Lpv977//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/7r5/REDACTED/REDACTED/REDACTED/1AZffb6/q53lPJWOVkfp/qDpNbqvc/H+l7G+ez1Hyox9ykplkX2Q9C+fZ2r1N//REDACTED/REDACTED/REDACTED/o/REDACTED/Vj/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/2b+U5Eq3zFTNyAdh4ugFRr1/REDACTED/wCRRmfb3/7+voXCWpZBLLiJQrzZJ/REDACTED/R2FJBZ425aK5+Wtf10T2iol4y2iyTOwYp2/zIYKRJ92bZdBFE/REDACTED/2x9sNjW84QWN57wXC8IF/1mPfnUp/Xie3+z+r9LSUbtef03KX9kPMlpPK0/KW2nodgv/dUxwL/REDACTED/REDACTED/tcBinGyos/REDACTED/REDACTED/REDACTED/REDACTED/+/REDACTED/REDACTED/QtXhbuDpPP2RLpma9bMJ65kkkj1/REDACTED/cdN2/G1vQE5/REDACTED/27Wd+1qccFxhBP/REDACTED/REDACTED/REDACTED/4n/REDACTED/REDACTED/M2esVqItn9EMfB/REDACTED/Uqvsn4McK8Z8ZGz0/TdEKcfDe88YrVu6zTYM7YBnW/LJSy0vcopttTSttyaOgK/REDACTED/REDACTED/REDACTED/REDACTED/NsxpVEMgE9qI2ABqj4KrNKIe5Fp2FqbJ/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/+v/7TP/REDACTED/REDACTED/REDACTED/Bd8NelkYXzbUx+WqqJ/BlrdW11adqgb8Ck/9UafDpe1UA95/REDACTED/AmNsq8Id1B8aXvWUQtE/REDACTED/REDACTED/3tl6//REDACTED/KUxdAmQI5LQGM/REDACTED/YnE9+6685NbHXf5Zt3eqs/JELZedwPNwF2+p/REDACTED/REDACTED/REDACTED/REDACTED/YxzudIIUiEaEdbnX/REDACTED/pyyW/REDACTED/vTHn/REDACTED/EwGk5Ah/REDACTED/REDACTED/+lIhMn+xESANAVt6t8dcEp85/Jhlb+r/REDACTED/REDACTED/REDACTED/I6clAAD2cuH6V7IeO7+gr/REDACTED/REDACTED/REDACTED/0fXHcsqbd/REDACTED//REDACTED/VAJgFDUK9pemA4kk26RonN35z/REDACTED/REDACTED/REDACTED/REDACTED/fTzkic/ff7MpGVwTqszo/j4mQpOEUGf989N/sdPL/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/q25NPxG5nX+sHudwryMjtMS2Z/REDACTED/REDACTED/98T/7NAIPzUDjCFC9gCnA/REDACTED/REDACTED/REDACTED/0rsQhe4LEXe3S7ndqm/zm8/REDACTED/9/Pv7ofk06e/REDACTED/HzkMw/REDACTED/REDACTED/REDACTED/REDACTED/pzDTkeuggGfmB7ZkJ0OmVlme/REDACTED/2K8Vk7nWsQ/REDACTED/REDACTED/K3vlc9f//REDACTED/REDACTED/REDACTED/au5/REDACTED/REDACTED/6jyvLZ7/d2l/vE//REDACTED/3HcYQgiLgaF6TdZ0fSCqqZa6A9E/mqlkt0cNdkL9yn+gj5/REDACTED/vTZvtN6okQefjjz/REDACTED/dUHh/dXY5MKIwF9mCZ9waz4Xcf/REDACTED/J6+4Jpvu7m98tP3QrGj9eT9Kjz/0SYfrn4Xg4aY2/3+1mEBBYLq9pr/B8D/2D1u4zVY619eHo4/REDACTED/n1M773OCpt4mVxtSf/REDACTED/REDACTED/REDACTED//REDACTED/Y5Ke4lR/REDACTED/G2r/1AJyeKN+rvLzUjwUP+h8h+85huf/1D/e8vfZO5Qwgr39FR//3j0j//REDACTED/REDACTED/REDACTED/REDACTED/ohf3K/REDACTED///TyR0dgBudnep35U7Psmrn/REDACTED/TTJsn19B/REDACTED/REDACTED/REDACTED/IEST5CvQhwE+Fh/REDACTED/REDACTED/b7+5Zev/REDACTED/REDACTED/+j67ne74/REDACTED/svt83GfHf/8t/ESk/REDACTED/aZomLTIoKqNx/REDACTED/REDACTED/REDACTED/REDACTED/Xn//REDACTED/REDACTED/B10hPwHyKPHha1oK29FSSuiSJPr/REDACTED/OtnJtySXaR/REDACTED/REDACTED/REDACTED/Z92e9t/aH+u5PqAaD+3/fvUKyLZ+2ed7y0S0P1a/REDACTED/cPf/REDACTED/znczF4spgkJ7wSof6oF8/REDACTED/REDACTED/+vjBlsr/q/REDACTED/UU/REDACTED/REDACTED/REDACTED/REDACTED/r40nS99n6svkv8AAoaV+z6Mz7/REDACTED/REDACTED/REDACTED/cJyQgNipaYUAQYl8uR0Fod/9IMIECTPMz3VbwQIFZUtL/Zub/Bo6WkiUqhl/WixcH96jpbCgAAEABJREFU+gb4YQv/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/zL2uXHcjwtj7EugTHqwIe/XGf3p9b/9/mY/ffgX91BDPLCQ4RTX7jl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/iM1+OXKV/u6kBX1rmCnw52FCyx2y3/REDACTED/REDACTED//REDACTED/KvLINK/+/3/REDACTED/REDACTED/REDACTED/REDACTED/PmXX/76QEK+6+ARTz7UofKYnnCut1t/REDACTED/mjv0/HJh5c//REDACTED/REDACTED/REDACTED/REDACTED/Iy3ZHLK/REDACTED/REDACTED/Jjs/BtGkdi86j/GB/7G9eflv/7r//LnP//59fX1u+v6w6XtvLr+RmVST3sXLGivm/T275U/HOv777e/lK2qbtLY02/V9Z/REDACTED/REDACTED/REDACTED/DmDk3IAQK2ylsQMK/REDACTED/8pvwt/qpAMS2EbySe0Pb197/Spr7/REDACTED/REDACTED/REDACTED/Ux08baoK/tPW43RqFnv5mR/kDbpwPL40qP/9V+5gMopy3SecUciMV/fj/ir8VdsFJ/ft8Xndd/REDACTED/REDACTED/M1cLUsKrlIWqjzNLycTtALgogV/4xzvcG/REDACTED/REDACTED/REDACTED/REDACTED/TYXrTD+uHY0GCD3/REDACTED/mONfz79vfvnPvjOmy0gzmIt7q8PR79pz/REDACTED/ZIlSV+ilJzKeGPWwuEpEp6ie/REDACTED/cPAEOcbdxhNeOO0wn/REDACTED/REDACTED/REDACTED/W+qyjWFcG3KXfuwz8umTguI4I/REDACTED/REDACTED/U31/REDACTED/REDACTED/TyMi/rIovb/Twut+e/REDACTED/REDACTED/sm8/8O9ZnZa7rfO+5Dhhs9V/73sdy2rfuZXpaVwLE/DVj+LWCJYNPq25+W8EsvrHzkP/+e/qblDxs17B4+Fk+VqClW/REDACTED/REDACTED/gLhO9+DL3E1fMjpU+OWeGhkA/REDACTED/REDACTED/OXyelferat6Ma2wKRD/oF2FHEuuPfH/REDACTED/YT/V7mJLjUe4Vjyu+3hiH7m/K9tCWEQ95gvrQVaeB4/REDACTED/zpfSGa+eafHXB78ydrfMbS/DyYY185bhaz4zPn1+/REDACTED/98raJjoHUCXRiKfLC/REDACTED/REDACTED/VviUOedGj/WF7gk/dZ+vV7/8Mc//REDACTED/REDACTED/LbsaNdlB+qtS1H6n2JH/REDACTED/REDACTED//uNARP2lY+PHEq41XIxGH2IC8/K/VZuxIfv1UWY/REDACTED/REDACTED/MNnm7wP3iXelZp2OT/P+/REDACTED/REDACTED/S/REDACTED/REDACTED/948vHL69fn6xVqyfpeFpvQ/lH1B/LuUP1iZrL2/W335U8Z9Zr8/6O+uOa7+v/1ngs+eeqA3b0++X/v8YA//E/I6B1OfSOy/REDACTED/REDACTED/uXDE2eHNXtO9h91V0NIJZNwETnNxFREC/REDACTED/0aet3Pvrwe/REDACTED/REDACTED/mCRwboo7aexeXrMkqcVawHhZ0vQh0/REDACTED/REDACTED/REDACTED/0vf/REDACTED/REDACTED/REDACTED/rvNne39H+4+u8K1xE325/93r+2n0/r0Of4zvqYI5O6yD7vpzq3xiP/vxP/REDACTED/JHPuBvt3EnL6mE0vwpHhUsQdVE/REDACTED/mQsJMMn+lwI9OFmdqj/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/iMeSShykCPu/RPTrtP24aPEmn/REDACTED/REDACTED/6TyV2fH+u3qc1J6flaf5PPj+V7/+97LGw1A6891GDm++cwuN2nbU/2Psr+/fbmyQC+/Xc//7I7QGuf9oFYvDlbq55wYTM/XTwtwRMW4/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nSTRD+pO2kG/kS0BuNuIGFe/REDACTED/IY6NUyZ5uBMYKJWNojx/hH61/REDACTED/rfXZqWfcfeXttvr/m/y/pzDW3+VnP/REDACTED/REDACTED/REDACTED/3x3ALPwdWh4zab7FtNwWi+/REDACTED/REDACTED/REDACTED/HxlAmQb9157sw9TTrv1/GOEkqTfBukj/REDACTED/REDACTED/REDACTED/Ekp1Dt7ZUCMP33aH+YWPef7rG+3d+3T97m99/7WK+t+l69+1uf2otN/REDACTED/z3rbM8l4Ksfjrv8uVIRr/SEnqZJJS8rhxAw4gJgSjpbFmi4ptwfv8kx/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//nj93fXysz9IRJAH3d/AnYM0oy5aFQSkyqdt5gYD/REDACTED/REDACTED/REDACTED/cDY/REDACTED/REDACTED/REDACTED/1T6/REDACTED/REDACTED/iAVnn3hX61i6Ru154a29R640plzOuIv540p6nJ/gmZ0BcjeDNvEFuy/REDACTED/XBQoCts9Zq1T4lbhAikkCw/REDACTED/xS+BlQ0cDbg3PDD5IDsRYhgDs6l3rvHLy/XjTy9/REDACTED/NX7hYYyZmYS+DCJgJ2FzKI/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/o5EyotQF9S+6iItA/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/3Q5O2ROAQhCIZK8l6/REDACTED/REDACTED/REDACTED/kCXt3nJAz+c25AWHyEPhHK9Vfh/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/FJZ/REDACTED/xf9ervXxYdFQJ9b/REDACTED/5ja/REDACTED/vMqKxn9XeXc1Y81pRz/REDACTED/7/REDACTED/REDACTED/V00aQBOuH/REDACTED/REDACTED/XvlJVQbSRRZG/REDACTED/kbm5kyQB64xF/REDACTED/2RGURd5OotcE3tzJQd72J5cfx19jvN76/aAE1qpD6vUOBqMIaLrFeMZ/REDACTED/REDACTED/cVVV3ZTUh55fPx5fPEygG5l5h2iq/REDACTED/REDACTED/REDACTED/d/zPPf01GLyFrfw1tl8m7/o54l8rz1/ZJ7SH8oTfsny5ElxBTUqjj/5sZ1/e+TrCrr+Ie1tcR8n/I9of6y/REDACTED/I+z7Y52DeHf9XOof/uX/REDACTED/REDACTED/REDACTED/uDj89Ia9k/REDACTED/REDACTED/mlbdEbU9LG+rSWYGpN23JI47/REDACTED/REDACTED/REDACTED/cPLn9Fpmjy7fZGZuMuS367Pn/REDACTED/REDACTED/IX09tdtPckwhe/REDACTED/+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/GhYh1bgMeJ/UkIM/REDACTED/REDACTED/REDACTED/01Ka91ktk/REDACTED/REDACTED/V03uVY0b/REDACTED/lv1CnaaW8fVa/REDACTED/j7E/REDACTED/CXsFJ8DmRizDkIN5E4IS4zvJsz1ve05swLJH/RTXheZ5h0qTBZDtrsX0v17WG6/jy8/REDACTED/REDACTED/REDACTED/qF20b62Qm8B1sM/REDACTED/REDACTED/tlumU/REDACTED/2YhclzQt7J/REDACTED/REDACTED//uH6MyPeWtdVEPcnzyaw7uJUDC/REDACTED/bVrvedH/mku8/jQdjhTRX6ylygpD6nH8/REDACTED/YBtbPhva8i/REDACTED/REDACTED/gvPDBwt/ovjDnQx+vc0Pah8/REDACTED/REDACTED/EB0P5IbLdWilJqU7lztaOdOwBhaa/REDACTED/REDACTED/REDACTED/6nm5/REDACTED/kkXz831HEsm7uI3Hi/REDACTED/REDACTED/REDACTED/REDACTED/nh9Pp/REDACTED/REDACTED/QW7wCex/REDACTED/REDACTED/REDACTED/fXr464plXm4a7lh93Vkm+L/REDACTED/REDACTED/REDACTED/REDACTED/AjjkWFu/Hq4IPURlh/8ct/REDACTED/yoRuRpzuj11WtAUUb+mFw7upVlxCCi18NR/REDACTED/0LQy6uNaaKlVZVaigQBmQgGBvKSy0/REDACTED/bVZaff/REDACTED/REDACTED/REDACTED/hLHbvlYjMObQHK/REDACTED/REDACTED/lriR5/KfKMwCCOThdZnariJp/REDACTED/PD4/REDACTED/REDACTED/nrTEJek496W3kb/tYcuyqXiWc8Qxkng56wh/t0r2VJalbX9LHj1Oztz/REDACTED/xDQmkJHFy12L/REDACTED/REDACTED/REDACTED/zkZ4Yrr9iOFIF+/REDACTED/SjFZ4pXhZJEkVu/REDACTED/REDACTED/KQjp/REDACTED/REDACTED/5Pv9DnmMXU/REDACTED/PTX5/REDACTED/5/REDACTED/jhzdS3DPt7n0H5doOd/REDACTED/RtiggCQ82hSmO/g0hakfxiZ75QIt8KyZb6/REDACTED/REDACTED/C+2wgy0MSBcDobd7I/REDACTED/VUcDoXAMtw4yh7mne9dre/REDACTED/8sP9d6yJNquEDsXaCQ81Rjsw4/yVsfiBhmQVTucNQYEacYZ2/+HjcmpXsfmv/REDACTED/REDACTED/REDACTED/eal08lw9njIGrFT9BkLr+e2qqvajdeF6/3erYy7oYAy/REDACTED/PinTw9/RM38x4/g/REDACTED/REDACTED/16n3+2J6vmL/REDACTED/szR4leVcvIuL/REDACTED/REDACTED/1G0kIw4gWN/REDACTED/REDACTED/XFUJu/DGvouhNqkHiTiWftbHAuhQQRt/REDACTED/goYqy5NMWrKlhhXWctcdGvTRcea/a3wNVw59Hz+w/REDACTED/REDACTED/29Ll8aa3dkbPk9Nq/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/1o/6tOfqx/8/REDACTED/REDACTED/X9mOu+pA5msJTFEb7RAgsmQ9WWyHW/AkdtCTNyGWcfI1BI8hzpcmRf/REDACTED/BYyjW0fHOY8/olJ/3WVcP+myY72KMRV/REDACTED/b06PZye5A+U3iu+k7+5D9iRa+KR3zyEkkzc6r/53QL+VT0Ad0u9Xx8S+f/+Oihny8+wBFQer/REDACTED/REDACTED/REDACTED/REDACTED/3B/Wu6e1+fnpyeNTpP5EQ6Hm/MuPAwvstY+LUP/REDACTED/Hxn765++WWv/REDACTED/REDACTED/6/AMM1FWzowB51E/REDACTED/BSXOkTsyHZpIeeR0/REDACTED/n/REDACTED/REDACTED/62w11/REDACTED/1WGQR64/REDACTED/E/REDACTED/REDACTED/xYJJ71qJzfSPov+cs+kGid/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/5GPH/4UpptDrg/4C/aLX6B/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xhhdGYs9nr80/UKc7PGgwdU9J+C1Z1F649T54lS/+/REDACTED/h7jSfxmtQupKtexm/REDACTED/iVDCiW3svokfKu/REDACTED/REDACTED/REDACTED/REDACTED/YCF/bRrxqUK/REDACTED/eG6jsaeL6Xten/REDACTED/al98V4GNL9y9f8dPX/REDACTED/REDACTED/REDACTED/eL6rlg1eGmm/kCSKy7StGdIM3rmk/REDACTED/REDACTED//YusmGdsolq/nlb4hpQyBsNs0DQa6/FS0BDbLpDwZkmclxAJZ1l1DKFLz+cf//REDACTED/uBb2xuNdEUL1Cdbw2zzXrq7bdliHC6NvVu/REDACTED/REDACTED/REDACTED/Pzz/REDACTED/Of2LTXs03hLLsUn92Z/JKUDAjNkd+COqa3pK/REDACTED/REDACTED/REDACTED/5sIRdOz3TW/REDACTED/xUMG5ebYA5f1t0t68u2Dd/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/xPkZzMRehJakzq6fnT89N6d/9BKvsAL5bJh/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/+EI4DeOz/REDACTED/REDACTED/rSpWmLyHimd9+eshf/REDACTED/REDACTED/BqoRWVhfvL3J9kWE/REDACTED/V06/8NzvS7uYv/Dc7/I+Z4D3et2bU6/z64/R/REDACTED/REDACTED/REDACTED/REDACTED/XJ+PM3flb9Sj3F7hQBu8rXPlyE/aFgMNhG3QebqLmSxMvhW1o/8oExhZL98FqWCqHtYh/REDACTED/rbNQlVi2mFW+pTy/REDACTED/REDACTED/REDACTED/REDACTED/PgpeeC5a3M4iYzwwrjlnr9G4EbEbYbms55D5/H72sRZs8clqUsIkFMr5VHwXr/REDACTED/REDACTED/Jl5v1lp8k/1ivO8z/REDACTED/rHyJCV/gW1P97pe/g03hO//REDACTED/REDACTED/TZWx8AJPGnW20rNW2vwT236rCf/REDACTED/Zl0Ukh4nHicGEzH/50POZNBjmr/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ViCVir5bZ/65YuXBx4f//REDACTED/TLDH/3FjNLSlb3MMW/GcGT/WfGXxNpyJHmsMy1eXeeK/vy/1NnjSFj3T7Kex1HsFX2nAD/REDACTED/REDACTED/V0zsjTKtLFAxGlwl3FnsAI+NzwYNR0s7lzy13/6l99cnv3Tn//REDACTED/REDACTED/mEJ/REDACTED/FovfGj2PX3IlV/REDACTED/REDACTED/REDACTED/O6wP7E8Pv31x8e/REDACTED/REDACTED/2a8araol7+DXpPgq0aLdK/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED//Dh9IsPd9/REDACTED/PD54txcH+6a3EgaH3E+px3XQsaHPaI/REDACTED/REDACTED/vfIw18yYZ/V3mHJh+/REDACTED/REDACTED/REDACTED/cJKMv4Uw0Dbu2rnNzsae/REDACTED/REDACTED/REDACTED/REDACTED/YH5pvvNVwEm5il7GLGGHx+/uuFM/362/REDACTED/REDACTED/KMtaVT2kcCOHZV8s/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/po/REDACTED/JxHt5oAAiEa0i/hflcQrUQvRmex/REDACTED/REDACTED//REDACTED/wosJ/REDACTED/REDACTED/REDACTED/2P++XjNn1wHpgPqyDsO6aTs2aGhg/REDACTED/by/REDACTED/REDACTED/REDACTED/TAF+9O8Vk78+rskjbFCGxi/ONPr7GD23lpP21oW58+NEsb7aDjvrs/tdqPzFidE42DUZhWf/REDACTED/Pjw/On8/REDACTED/c2fm/REDACTED/REDACTED/dbYfua6Tvh3ELJrYsc+otf/REDACTED/JoNuz3LrzhIXwe+jQ4/REDACTED/REDACTED/REDACTED/3dreZvQTDqqGJ8N2yTK/REDACTED/pJXpD8fG+/REDACTED/fA9Vm/REDACTED/REDACTED/q0+YG7InijR0EhC/REDACTED/bvimJKUzfyyhK1a+iKdCE1na/REDACTED/REDACTED/P+n18blCL55vI5Sw/REDACTED//M2/VXvQeTtjNW/REDACTED/REDACTED/REDACTED/UX8rodjK9YMT9ixMsK/REDACTED/REDACTED/SF8ppDd4j7EoIxdh9qXp6ef7is/REDACTED/Y7+C/FdKlwrLV8Lhq+DLf7/89b8JJC/REDACTED//REDACTED/amfKQmaFxbLKz45gZW/6HDx/REDACTED/REDACTED/3YCo33wnGhmArQVvpN5d1mlls/REDACTED/SSuGBwkgDpa5nsuSh38cXOC5q4U8/rUv2yS8AQq7/5xX+7v/REDACTED/REDACTED/XET6rxi5RZFbMLc8GZb/2J/REDACTED/REDACTED/REDACTED/mXMh+XktL9ZCHrXS1CBJDH50+Pzz/Gqo5o3GrhTvktIsBKWABLLUO/7/REDACTED/REDACTED/s/zKdab0trwyX1+Df3kB/7prplzF/REDACTED/REDACTED/g/REDACTED/K7GpynZvbFIqFebjMJmDy0k//REDACTED/REDACTED/CyzfffLzAP/REDACTED/hCdhvJ4l8hE2AkWfhzUK+b//REDACTED/REDACTED/REDACTED/REDACTED/RxokE2SO7dyOyCXzW/REDACTED/REDACTED/zxeey8XbDSo7yKLs2sAEaO/REDACTED/REDACTED/v7+kvX0+JiTKtace/7/REDACTED/xM9RaSLXQeGfWf/UrgTF96U/51OMXgK+BO53wN3DDYwTmk7wkPen77bZJ/REDACTED/REDACTED/REDACTED/REDACTED/rfNV/REDACTED/W0bPvnEIPaFfcOOP/REDACTED/s77wtvg+W6HWjo4NJUAqFatIU/rj5fx+MWHf7q/REDACTED/yelruXRpI8OTyLjZbmcnEMKxpEEbmEi/REDACTED/REDACTED/REDACTED/REDACTED/y59///f//uc//REDACTED/REDACTED/REDACTED/vw4ZvHx8+Pz89atMFb4Jhl4AlFQ+5M0Jh+h/REDACTED/3m34NqsPFG3FffeDhDF/REDACTED/lbsyTW5HhQ/REDACTED/REDACTED/REDACTED/IXH3/REDACTED/REDACTED/REDACTED/REDACTED/wHVf9zmSRLaXQi9XE81/REDACTED/lL79/eHj8wx/REDACTED/o6Ji7R86rP2Va0RCu021saC0/REDACTED/REDACTED/7RqGrs1tjzFs0q3KS4NslB/REDACTED/REDACTED/REDACTED/REDACTED/8s+mHYH8JvSbz5+c39/9/T0/Hlz3MwG/REDACTED/X7gZvq5gTnzxiFWL0/tnHt7Y/REDACTED/REDACTED/E8WXiueUrZRTVnW/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/Pzk/REDACTED/REDACTED/V1+eWXhw5ZbE22ivH4J/REDACTED/3sNd5BF9pww3wVx6vEfb3jnbc++Nnet/vl9P5F9DDa/EPlN3oUNBf/REDACTED/AKS8ESKpZAXC3eqnABJkt6MQV6lntD/REDACTED/REDACTED/dd5WQ4A3yWenWmRBvWboFMDgRkfe+y3NCeF/L1pfI52WYe/aVeN9WP+/REDACTED/rq6pYCt7w2BtRGX/zgYIoxZ0McFLzGhyWkRMBiyWO3LxB/REDACTED/REDACTED/ooW/REDACTED/qXfGLjgRr9dt8//z050+f/REDACTED/z+dv0v4j3enmcdynR/r5CL+s5695KenNdoH9HdDJ6/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/w+Onx+a/REDACTED/BO/REDACTED/REDACTED/REDACTED//6nd0xNNXD/8/REDACTED/REDACTED/yg+3LJtg5/REDACTED/DLMJrPZqjW/REDACTED/REDACTED/I7XEDCdDUERp4S1yHlneoNj/AhhI7LZd/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/XMEv7Vp797M25ofU/CV1ex1datz/wj+Wvj8W31ePY4DD3xlWjnqa5qj3//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/BARZeEjzkZi1m8w4bYc20Ze+/REDACTED/a80CXLFfgWGwKO2k/xrYRlM4oYJUfGZxQOVs2/REDACTED/t61B1JF0npXTSJ+tMApUuR/mQt09/fPzz4/On5/PneHr8DK/Kj9W/VnKsf/2uUiscIgm0H1TZM+gQP5f0d7///Z/REDACTED/gr5YGZU/hA+x+pTe/REDACTED//REDACTED/h/LD2KHHEKLggXB3K/REDACTED/REDACTED/REDACTED/m47OUUa+jpj2VBKQ9ApW5kY/REDACTED/d0KXD5VRc+u/ZrZYDX3NOm2/REDACTED/3s7yGoV8P7KFejN/REDACTED/Pnz4//mneEpm0sOlFRp4gUrBHMT/ymSP+MwjeF8sjh07277//7uHh8enpKYUV/0ylnf7U+a+VOzV/REDACTED/5vgNTjGDL7Ox3Z6Wqc/REDACTED/REDACTED/pBXsjZ7APhh4lBhT1mOVHli/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/BU/Kmo3v8jGSsOryrlR3bhpj/REDACTED/liB4SRp+lYjZOnNIb4R1+oUOOevpSRZy/REDACTED/EwUretHwzBjjOZoh5GzGEKsAI/REDACTED/nz7/REDACTED/REDACTED/q987N3SmquSt0Hut/6c8IiY8wbtw8TfOA/REDACTED/SHTC2Lq/REDACTED/4vPKhrfiklS90V/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/j7NocON/Dkz7yRDDOSLO/REDACTED/3eiqjvlx9/fPrz0/On8/REDACTED/NrUP/REDACTED/REDACTED/07MVXkTAPPPVqnuThR/REDACTED/REDACTED/REDACTED/8oh3/REDACTED/REDACTED/REDACTED/REDACTED/S6/ka//REDACTED/REDACTED/+DaupZcy7cC/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/C3Q7ajHp00rZJmk6fEOpaJGjTv/BGLR6Gse/d5YMaSqkU/REDACTED/o+Pf/REDACTED/REDACTED//REDACTED/REDACTED/Oe3CGEuFqTCJjM6RLhUtjC9TPSy/kHNYOrDyo5HItV/REDACTED/gcQecAWGsXX82w/REDACTED/REDACTED/8VBF5mUz+/REDACTED/KQGVUQN85v1DLNbg2zWZ17uBp6p8Kv/REDACTED/REDACTED/g1tfuusrYkWuU/REDACTED/REDACTED/REDACTED/NkNocuHu2/REDACTED/REDACTED/REDACTED/aZ8vs/REDACTED/REDACTED/FpNuNuEvF+Za/kf7zM31Bl/wzVkcv36M9TYiVcVl5/REDACTED/uHy5/Pjnzl/REDACTED/j4cFXhfx/LbJgPS4/5B/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/jUNL8tP+JTohTBkqyRVtDa6OqH/REDACTED/REDACTED/wfMn89PCfPfWUidS/REDACTED/YQuWD6CX5H2OnyQpuWySp/REDACTED/EF/+6//s1m/REDACTED/REDACTED/REDACTED/RhVwqcM0CGnpv0BJ3LH0d0eIQ6O/REDACTED/REDACTED/REDACTED//REDACTED/REDACTED/qpNyOnpmcH++buishc/REDACTED/REDACTED/REDACTED/Xx8+MPbTX4YwtcXz/m/REDACTED/XIyuZY/REDACTED/Qr8BN0QzTgm+W3Qg/REDACTED/0p6t+67yRsUtpRPiXfMBKarRufCqKUkZ/Exq2h5jVgM6sld/CV9EZ++w6pvCmd1iYzgbrH/REDACTED/i6TjKDQ5+5pv/REDACTED/REDACTED/ZKT8IWC/vX3/5fwLtrtPnrAvtphNeg+KQFrFB8+fjw/P1/REDACTED/REDACTED/REDACTED/REDACTED/xXjS5hlYMEzP4jmulpTTg4H+heYr/T01H1giBdn0ThQV7r0c/tx42pi2gfd838MvZcB+ITW3DA/REDACTED/REDACTED/E8eWde/REDACTED/REDACTED/REDACTED/iqoeBjqSc1pDwNbaf4sqK7XbfHz7/REDACTED/kghfXAA/mm1BN9Aac/18/REDACTED/Tqj93hqXn3QIf4/Pvk/huGtNexxvh16T+OYJnTbs91d/92/REDACTED/REDACTED/REDACTED/wCcvo8Zzwi0/REDACTED/Q0lB+Qr4d4wkQjTk6/REDACTED/9L7W22TWzf6WyWDm289onx51DEC9pPVny1/a/REDACTED/1di+UupbJREa/BFO+vwRzwnb6w1p1jzfC1/s49ncCV/1qDx/pty/CmEo26Jw/Mbwf39fCazLbHn5HvO1xVQL7caxB/REDACTED//u/REDACTED/REDACTED/REDACTED/l2keH/REDACTED/REDACTED/REDACTED/G8oP/REDACTED/9Dp3qp+a/oSGR6Rkv7u3/REDACTED/vuhtRp6VX3Bi+p8nK8hOM1zN/QKuf5iu2dbZSoI7nq7CNYjd7Yeqq7K9eX/REDACTED/REDACTED/u8i9Zwp/zDGobJXV398vT0/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/+q8Pnz//5S9/REDACTED/REDACTED/tf3S0fYP2KlSGMv0G29vHbu/OzPT+nW1Cl0pBN/REDACTED/REDACTED/REDACTED/REDACTED/VhX+F1S/xzBP5tmvr75ryZJpDcZ6gLue/vK/76hfz+fV4/v+3kI/REDACTED/JGe/SB2Bp7faqDM3UU6NejdIvkTkf/REDACTED/REDACTED/lrLc/REDACTED/REDACTED/REDACTED/1t30VBSbzSp+jTRgf+AbX1TQ0+P/9H/9vMEENTujGANf/REDACTED/C6+gcDYlSJa2Pun58fPD385nT5+vPv+tJykCp+U35n3/NeHUgC/REDACTED/9sOikU2zK/REDACTED/REDACTED/REDACTED/fll/0GUke0uVbyd/REDACTED/REDACTED/ALsx4J29FnsFGXf3zff+ZsV/REDACTED/REDACTED/REDACTED/REDACTED/WhvW/REDACTED/F1/REDACTED/enbb+9/REDACTED/REDACTED/3EGMVxkdGh2cFRhpEhW68iSuTGKuDi//Hhj5fX/fjwX6R/REDACTED/8oP+fvz4ze9//7v/9b/+15D/REDACTED/vB+GvoAMb0lf1FFlIM/KJ+2Wl9y0Sqw3rRjLDrd/t5QYn8Mxtat84FVpGTD/REDACTED/REDACTED/oyA0L3Z4n7Rlt/REDACTED//REDACTED/qeze0b5/btU/LryHfwGsaUW2O80+Pf/z08J/lDTpriPZtVUGTJ8dbLMo4I66/REDACTED/le6idz+OukP/REDACTED/9U//BmSF6TuarXmjo1Dgl7s1JW/tq7KEkpR/REDACTED/REDACTED/rv3ZD3g1/R0Zvzu/I0ZCvw6+yH/726y4fjiN/REDACTED/REDACTED/OhEu1p+X+w+nbZTmlyWPlpR3Dt/pi/REDACTED/REDACTED/REDACTED/REDACTED/0/O38Nf9tmTbYW/PL0a4flVZHiQFv12Ar96u/REDACTED/+V/REDACTED/REDACTED/REDACTED/REDACTED/wB6Z0OZ7C/yi17kZ0XaPPBVYuTz/REDACTED/REDACTED/X2oeGirgEBWPKN5gz+3/L2NHGzx1p+qanotfb13TURmb/REDACTED/VP1GbHd6PunC/TJdztnLVZ2Rlivx4lcy/REDACTED/REDACTED/REDACTED/4dAdI6rwXu10xysV674VUSKllG+SqluV/REDACTED/REDACTED/REDACTED//REDACTED/hViTMJJylZzbRXHQ/yXyGc70bwlnIaSm/lJdeSKOLMa7Z/REDACTED/REDACTED/vj0p7rbOR/REDACTED/REDACTED/bgbLO+P2TZ/7+7vf/Po3f/REDACTED/REDACTED/REDACTED/REDACTED/OG5tnq4THpXU8AV0zJI98K/zuvzeX303c7el/qJVQL+Vpj+vrh1ac6vOmuO4FcJm4Qr3/ty+DjF0B/ANc18LfnR8orJAmsZw3Ekj/REDACTED/eHp+/sJ6ckYdwsWyA3ycwnFcdUemdA3PYVUpOd07X0wvn3/+l/REDACTED/REDACTED/kx6/REDACTED/REDACTED/REDACTED/q1avHZs905bIDF+WuYFhRm/DY+4BGHj4o91gMjxe/s2aIF0/REDACTED/sbb9LuX/exA3r8Gvl7+PZ0laObyw/z/V0DUl7Z/REDACTED/gm/Ds/bhpW7A888t/6Zx/zIPkGNMi1JY4bGVaSX0s+iWcT/REDACTED//d3Am/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ml8gn/REDACTED/lGn58f/REDACTED/REDACTED/REDACTED/REDACTED/987+5XFYpWkBRUeL/REDACTED/REDACTED/REDACTED/mIDI/REDACTED/15v9o/REDACTED/REDACTED/XGa/REDACTED/REDACTED/j/REDACTED/REDACTED/REDACTED/REDACTED/DctOak5wbtaSq+WERsi/REDACTED/xua7wFYnUscs62d91ks/REDACTED/REDACTED/KpxLrR2fQDi0p/REDACTED/3x6phfPgpa1Mcf9pebKUmtG/dvqFWG/3C21F/X3u1/Y4/3jmHiAnh17T8S6n9/REDACTED/REDACTED/WEGv67vh/BVfamDr+hd13W2ps+/REDACTED///C//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/yXSY7UjmuMvMiWvFz9WGn/REDACTED/9nnH1LXe+QLjcZDw2Ygohfz9/Ak9d+P4PfE888t//REDACTED/6j+ASDvyFQAFubyz9oP9bQth/c3Gqg0FeBvdGtWw0/REDACTED/REDACTED/C1+jjrYSTta005pm/REDACTED/REDACTED/REDACTED/REDACTED/xr8EzmWPob1VQUsjl/REDACTED/qr5Paqt1qlJREonACsGwp2j/VvUynqtJhe6VXUHo8i/ZKiApV28wnrL5+5fm8a6LUk/aw6sPTXy9/Pz//OemKHZY5omq+9ejU3p18kF/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/3b/W3VK+OvTjm/REDACTED/6XnZK/0d6kNOd1qnqWhNZ1bUxru8w/REDACTED/Fv1sLVO/REDACTED/8J5Ds/O5e1VrY0tHFTz5a/n/TnhPj0xAJj53m7RrRGqJ/REDACTED/REDACTED/y1mzO//REDACTED/Kv/TdBvcn+PzE9OOfr4+hr9wt6/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/lapT5V5lIxU/REDACTED/REDACTED/REDACTED/REDACTED/1r7WEsd1Cm/REDACTED/iwpaV8oE7ZD4A2+QTJuVGB/REDACTED/9Os/REDACTED/REDACTED/REDACTED/6Xg7c5N2TEDq/aXqm2IaBt8JD4g/REDACTED/nMsn0aW/pnuJh7v902p/REDACTED/v8QWOY8M/aSwf5QNvhj9h75/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/w+aRt3pskMxGcO9EM1u5UzTG/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/v33/2Pdl6kHFgh9loXM87tdDglHub0ax/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/ifmNddMrFFHEo4qYdS/XaoVPsula5IGcwl6BB0P6DTlt2CvDT80/REDACTED/REDACTED/REDACTED/uKYN+qiwnuncHCzV5OV/Bb/REDACTED/REDACTED/REDACTED/0ItMxq81m85/LkV/REDACTED/REDACTED/REDACTED/REDACTED/3mNaGeTcs0NqaZw4a0wtejxy9f//REDACTED/REDACTED/cvfCEYmj5YOnM/XlIo1HXAyws5Q0OY/xJFewTc5oYBhELYtsZhjmJQEdL/REDACTED/8glN4fA/REDACTED/C3lssPlQJF1Z/REDACTED/REDACTED/BQOkOvJF02uEiUrpexsF8QX+Xu/REDACTED//REDACTED/REDACTED/VS/5ZlpfZ4JfJ4Z9f3vK0fDInEgxIFhiE/6WwRp8x134aqm+Pl1TD25spf/REDACTED/f3z//Hkpb/REDACTED/zw6YV+/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/LwP4r3E/NH727lvqA+w/IT3YkiPpL/REDACTED/iz4pifinh1NEUoOSCuPO41L+ceL0/uC/+P3/2NlaLYBSJ8lKfD6RS9zi1/REDACTED//Mu/vPQ+/+t//REDACTED/ggxZ9//REDACTED/REDACTED/REDACTED/jF+HGZczPSx8T/REDACTED/REDACTED/ct/vDzylX7/evncxkWQiuKaz0xBNx3q8o5obI/REDACTED/faF/+9u/vfJ770StuQ3x/REDACTED//REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/DADqoxAEsnVgXNv/jBXy5/REDACTED/K3PuTS0spn6ul2er3GPmnwJv3ll18+f/78+++/b/dHp/ihv0O9v1f5aof0/REDACTED/REDACTED/REDACTED/REDACTED/k+4FZhwDpXKI6Uypl9R+ydxV/REDACTED/REDACTED/5kOh2A4mf5woGsDHJ38zHW/+OVWgU/o//+f/87e//ce///REDACTED/+LogN/REDACTED/Im/REDACTED/REDACTED/vOC/REDACTED/REDACTED/AvOmrGYs98OLbQNsO2HQ5ypdiis/yFvgs3mI8L/+3//REDACTED/UyBLz3CMb7FTzn+EX+tETPwyWw/REDACTED/REDACTED/IT8uRXxBTCPkn6kHWksiz0sYxxho/REDACTED/REDACTED/REDACTED/gp6efn59+YJX/REDACTED/KZ24KL7O7X+t65pQft27A65oajZF0yOOp5fMK/REDACTED/REDACTED/FNM4dsr6r2dHzP8n8P+Mp6vwflDzY6wdMW/bgrfQFxvBL/Lm38xQH+H2AuthQc42Q/REDACTED/REDACTED/REDACTED/ueLhl+KDNH7oVCQL4vKS8SHSlP0mXWo/REDACTED/uJ3g/REDACTED/NOnp5+4vFff2HLfPtN4kt2f4WsOfbg77Ssn+72V+7X8g/m8hvkl05+//v1Sfm8TSaF2RDyp5wNCG/51qOXxyhK71+eNX/REDACTED/REDACTED/5XTeVJO7kWnduwdyx/V3k53/Jp/REDACTED/3Y71MK82zo/REDACTED/d02m7J+A/z+cyk44yY/REDACTED/REDACTED/REDACTED/BH9jFVWU1eN7fW/REDACTED/PUv/REDACTED/sv29mob6lqXFbMkDzzixPhR+TT/REDACTED/REDACTED/ImA5rdowy5IUQAl7L/REDACTED/qn60vbq4eckXJRJ7ic+l1exPv7OVWP2i/VaFWlV2/REDACTED/REDACTED/iz2fmGE9dyTG/E1ecx4v4++CY/sBMcDG2Nsk2zhh6b/TriRqyrOjinYma9S/REDACTED//OVftS+Lsz2Nso1UpNJyLm/U75z5MJ4vZg8XjDjBUmSRH/YJr/REDACTED/REDACTED/REDACTED/REDACTED/KGkz/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/BGTLO+P/REDACTED/REDACTED/REDACTED/GJyg/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/uU1I/REDACTED/REDACTED/REDACTED/PxPf/rlT3/6/8r//REDACTED/REDACTED/Lnjc3ynWncA4k/REDACTED/REDACTED/REDACTED/5v8nOe3kPm+EgChMcgK3gb/GQLN8ga4WAc2tJSM2DnngA7u5WPIIXA//REDACTED/FTYzXpm1Mpd51XQI1/REDACTED/REDACTED/REDACTED/140jA0fh3zGP758fvrp93/84/REDACTED//REDACTED/REDACTED/JifZ0iW59MxqLVuZtO2r52cabXI/REDACTED/REDACTED/K+9qTuo+aZ1R4HgBKPQm/qo8asgqXHRAota8CovPbPuKbOg/REDACTED/REDACTED/kLviqfGjzWw3Od/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/4dGp/aStDs1mUU0+xsv8ySUNFp/AfN1dJ/D6F2yhN3tQoPEAQV/REDACTED/REDACTED/REDACTED/1Ao38SPlgLs/REDACTED/baEvIS/REDACTED/REDACTED/aGBrwcQeAMD9/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/oI6pW9ENQ/REDACTED/GRn/8XUPxiGU+4OunV8/REDACTED/B6Q/REDACTED/tR60qUnFMBc2dXa5sXS0oZ0/KDUl/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/nyAgiopqymYs0q8g9oZ/REDACTED/REDACTED/REDACTED/It0VWhSHPUF5hi7V2hq/REDACTED/a/7e+/AfNvF2fELuFjwU9MBvs34LHkQ/REDACTED/REDACTED/REDACTED/REDACTED/OtPJ1rEVCytgPiq/REDACTED/REDACTED/REDACTED/BZlnrqtrbX+qjPzkU/REDACTED/REDACTED/hL4S8+vnMX7zWR/LqF/XLp+Nthvt/Mh9O/REDACTED/REDACTED/Gk+BD52/REDACTED/vRP/REDACTED/qDJJwKC5IQzk66HBsEAWrHl/REDACTED/REDACTED/REDACTED/+vW/REDACTED/Kq5gXgr2Wtry8Gi2JNBIk7X1Jth7/REDACTED/REDACTED/REDACTED/KwPqhblL4brW/JMyxCTv7c0YVLaum5YcWlTCLnf/MCbWHqlB2NXjcqXthb4ohMC/wTO7Re3T0uObV91lOuEo5j15GKY9dW3eU/REDACTED/S1Y9rpeaVqIDpeK/jnf/rnaF2i32sKsCR3DnQoD9BLrCtF6fo3883/REDACTED/AK0rIAJrv6ROoEg0fFXSPY7r/REDACTED/REDACTED/REDACTED/hzfqcVAtM/REDACTED/N6cEAD/REDACTED/REDACTED/REDACTED/REDACTED/KY8z/MBQ80GDCF8rP0pH1o+PIw/bS9k/TgGO0d1rNgkBb2vL9bvH172KUm7ur/TXoy2cbi/REDACTED/TiGQ3i15XSQsRCKbQ/gJ0IHDCB2hdiKt+ChXQoU/REDACTED//xRIMbMRw4knOQ/REDACTED/REDACTED/REDACTED/REDACTED/p8w0n/+MiHzveed6HXzcqeok1fT/REDACTED/REDACTED/jjn/REDACTED/opQJE/REDACTED/REDACTED/REDACTED/kPcbblDy0/REDACTED/REDACTED/EKy7jDh4Uwx8dW9/xrjC5fA5keMZ/wJ7eDoO12Vv297Z7fY/REDACTED//REDACTED/REDACTED/REDACTED/RnCdm9d4Hj6Q/REDACTED/dpSyNOZ5STID/REDACTED/gY/grjxn5bxZX2+Gx3L7Qd+MXjeTPMS42e+E/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/oC1a4af957CYP6Ja3fGmdbR5D4w/SnekxyGzrXJKsaftiM092/REDACTED/REDACTED/mS/REDACTED/REDACTED/DPTwab71OyX0L+VY//IO+OEMlGT/REDACTED/REDACTED/REDACTED//ilR0rPhjiq3HMeJF54NVa7HA9/REDACTED/+n2hXU87rjD51TpIPf9n0M92/REDACTED/REDACTED/REDACTED/o114Pq/7r8RmL4m4Ueptn3v92siEa/REDACTED/My9Wu4fCI+1u7maXh6/uFnsWLQvaZgzKywYpQAUGc/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/QsgxS2/REDACTED/HpxA/REDACTED/REDACTED/hIbVNgoPykzAO+ZsfipD2Alz/wemX7tt2wimlYpAkmv80+oG2fz7/wUkUH/yPz8M+53XFPfFx+v727t4F5z6xxQf71vOYmn7/REDACTED/u/ojEqenxmZYRHshGvr/3COZ3RTwpn13qGQCAvSI/REDACTED/xLrAzq+R/REDACTED/REDACTED/53jw8FlpTbsg0/REDACTED/vTrf/zn30zv0WxpE09/o2iJECYu8fK24M9u465/PMH/wIxvKc/REDACTED/UAAAQAElEQVT+/REDACTED/0/lgTQvnWf6008//fDjj//+t78FS1gsFscv/3366a/REDACTED/REDACTED/REDACTED/Pw1NbFzz//9PXr5fOXL5vhi+bxYPl88D/4H/wD+mfAp729u8f39D5mr+8Mbzow0h/REDACTED/T8zyj8EeUMeVP9pGIm4sw9eg93/jjZLP8QT84v4uT/REDACTED/MiVF5/REDACTED/ILFCV2c/REDACTED/REDACTED/GuPn/REDACTED/4bfGR+tqkUZZoW8b28bYMt/K/REDACTED/7Z28a6xuyPk/REDACTED/REDACTED/REDACTED/LPnd6FsB3G5vEmuLsQ6/bRKZU/REDACTED/REDACTED/REDACTED/Ph+f7+1zp77vSnyc3nFP77e/REDACTED/eg/MHQl2Kyr2I6e1/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/u+LN2AozzPdfVVNLbZ2E532/REDACTED/REDACTED/REDACTED/REDACTED/nSwqRxVmN6IMbeNNbyxOz2o+/REDACTED/REDACTED/Qt8O9fDnCAv1Ff2/V+RH6u5mN4L+p7hce6XfOBZ/na3pmvJ89nvuqByI/REDACTED/REDACTED/LuegT5WPgwyY/+hFwBR8CHzo+BD7ch1978Mh5FH/NFQqfg0W+9b81eabHTGeC9dfajx/FaghVfu0dWHGj8xJWswxIRgrZ/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/C9lc0wzvD7oRCth8RHDPgg3/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/E6qNyQ5SGMnpTDDnQQte5J1BI/3sacwFNcq5ZlYtNUZ+U6Dymqlq7s7SN7D8cu7mqE/HYrM6VTNfD6/REDACTED/REDACTED/REDACTED/LGeAn3MwwJ9jOtow/REDACTED/REDACTED/Ncs5zE/4G05OSJvh+/XfQf37s7wcd1yBD/eNngQ3rYNaNcOuQHPbJ7H5/1xNLSR/bt88UH3+qZ6XH8AsyV2bMX+Xt/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/TqPg5puA+GGaYP/REDACTED/PtiVXsnMCRMjnEL2/REDACTED/REDACTED/REDACTED/y3wNhjkeGWD16RU349bmjE/REDACTED/54xzbH1R0Os1vu9sa3nGmKp6/eMuQs2+Xksri9WjC0ORhiq18U/8qdKQsCwh/3ZOl/lcXr77TGBHD/REDACTED/REDACTED/S3/HV1zErJlAtkiWXuVfdHvYy2S/REDACTED/REDACTED/REDACTED/REDACTED/REDACTED/HVc/REDACTED/REDACTED/REDACTED/g9f3LvLsjH8tBjn/mfGMrxgO8F/wX//ry5gsfP36GeZhFONhjDPM1f/REDACTED/cJBDFWhn8A3U5Ftw9hg7/REDACTED/w448///REDACTED/REDACTED/REDACTED/Rp0OR4emtIbPdvlblGjP84wK+XwiiM/REDACTED/4O8UzuX3DdvSNU4DvIRevSK2/REDACTED/REDACTED/REDACTED/REDACTED/ctzo/b3tUeSLkJdHgAUVeMdcFPAcEB/viFdwrDX6+BI34o/o+8hnY/Ds3p/P/REDACTED/REDACTED/REDACTED/REDACTED/cm/fo/YGPH3G5sZyvwfHzwX99/REDACTED/REDACTED/fxm+Vh5VS8AQjfnp+/REDACTED/REDACTED/REDACTED/REDACTED/yqc6Iz/yhQmKTnC/REDACTED/D9KXa4oZAwdBgy5gY88KdMBiJeiWk8/RE8+ik+SmtysGJkvEfhEAVk/1E0FTLFcxjQOJx3ghY/LU8/REDACTED/REDACTED/REDACTED/NWY3+M39DzftOsG/z6YdviRnuW3muq98m/J7z3rAg/xj8gJXSeHt7SLnv8+2vtt/REDACTED/qdPzz/8+NOXL1/fSXqu58dS5SpQ7CLGfPFBgmmgPwl/l2KHjept1aRRd3ht1/JFsFPIlFy/REDACTED/REDACTED/r58+cvXy9f6xSpxq5t9ud/+vnlNb/REDACTED/zccZf94LCEqriBN/REDACTED/vob1H/SOq6wBfv4TKuA9/REDACTED/R/REDACTED/MPBxKDlZGfFXzTF4DiHgAb/REDACTED/TuYzCMcOxZ2AjDlR+xerQcKOIgKjIIY/hGqu/REDACTED//OWv//jtt89fPssL5dcVv7SgX3/55enp+d/REDACTED/YE4pvuY3yFvcQf9IP29L3J/REDACTED/RmZ94k5e3Q/GHH/REDACTED/REDACTED/AV3WgzMb/loat/AVvxf+tfmalc+b0yNy9Tj8h6Hb/eabUE7bWfx90W0/REDACTED/REDACTED/REDACTED/REDACTED/PviSM/yP+jxcnscPiI/H/TeNOrD47hkPQydfj6Ox7V/REDACTED/REDACTED/REDACTED/Oh+3TLB1OEqFwvfelBW0UOr8/REDACTED/hk+Bj5+C3w6wKe78mnIh0N8eigf7sSnh/P3y/REDACTED/0bsXR8FrHw13hXfzOf3Ml/REDACTED/REDACTED/REDACTED/REDACTED/pCdj4FPh0Z/REDACTED/6EtnT5U8rn8/mb/mi3oVf6kk1VUxdVmOYJJOiIMZ8/qt1ze0FA1bifLg33+Qk4ihLh/REDACTED/zed8bfHxHfDxTvzXTD/cxD9Sj1fLyS1y2/REDACTED/U6PoH3HQSZH/opoNv4xzGGNCjm/REDACTED/N/REDACTED/REDACTED/YUD6itp63t1JExovew8JYQtdENXSvlEY/REDACTED/REDACTED/SJTfuU/wP/REDACTED/REDACTED/REDACTED/Zy0sbfzJlo6fKmMMqZcTpZTxaWmV/REDACTED/REDACTED/wPvI3Plect9fg906pL/REDACTED//AdiAYnlM6SKGSrT3A/MoG46cf/wI+uU8gs6/yGBpef70Bp+hlsQh/UFLCGAMO/REDACTED/REDACTED/Pv1ZmKPLJML1HuWr1xhwHffJesMjVDfhd1cUH/sDfEJ61I7qqPb433TLEnMcZ/r7qd9xX7uHYzzYYT/REDACTED/AUvM8A/REDACTED/bIprBCEefnFdSbB0fMOilq/HIr+HcJB9NMmJWEWBtjBLOgb+Fl64HrT/REDACTED/R8dVhh+CUXbEbfFfGdM3zn81/GjZ+Gh3e5hO4W09ibfgszq/70eO4lm/9jAc++ho7wX+oH+P/REDACTED/REDACTED/REDACTED/REDACTED/f2BKMG5Td8DX6Qc6hx9Lj+vkK/X/REDACTED//REDACTED/YoHKJQj2w1jwwx4/MUHHOuKZRG4GMopbE/REDACTED/W/FeuoCxKkf8xHftJHSiiOxulYi/gNgn3OzjC22VKqyz/REDACTED/lQFZ4U8xGeVZzqqlgatNlrCjRqv8RM/REDACTED/S2LiB9nw0+W/REDACTED/875NMr8ukkH94B/REDACTED/Am2+s2m35HggR/REDACTED/ePeriJVhDHwTzOJOAi+hA/etKnUMGh9LeOtHQOBDkOcs7S7/REDACTED/qHAopsphGwc/REDACTED/XW6ocj0UjihAdyjQ/REDACTED/tzXBJn+Dug/HkE/vh8fO4rVzO5/REDACTED/peopUdt5OFtyZlHWpvIImn4j/9n7Te0t0nwQ6/4J6CrS0NW2PGzWL/REDACTED/TwyXVE/tTL/37yXk/REDACTED/REDACTED/x/hOsvQ9tbUWX6d/Hqgb6QD/REDACTED/REDACTED/FwG+vKkAxjvH9KfI1xsKp+Knyi/OxwBgHecA99fF9UWtfu/gbotr2r8cf9HH06U78D7pJ6/GMZ566rr3M2t03QTnvM/REDACTED/ecb/REDACTED/REDACTED/REDACTED/fgx5TP+a8jhB/+D/REDACTED/92v0ZvQR8ph/REDACTED/REDACTED/REDACTED/REDACTED/Jb9wH/REDACTED/REDACTED/REDACTED/bZ9b8yv/REDACTED/1gCYcE3WHLPICp8xBX6Mh/mGIfBBvFCU3tRx5VPgk/REDACTED/REDACTED/KJ7r1S09fCOFA/wew4H+Cwb9XegHN/rNg/2v9uMw7Mf7fj/REDACTED/JTovwz9GoDWD0r+Ufab/I0D/REDACTED//YHmBoPOboSaNQCcLi1D5Uae7umO/ruQHSDDJmb7332ff5HKliAjAKAR/ge/REDACTED/SGhmG1w9x/REDACTED/REDACTED/REDACTED/+B/REDACTED/REDACTED//REDACTED/REDACTED/REDACTED/6Qe9Lo76FrJ9nOnwDS8yOt/uRR/dlQ3yk/REDACTED/SN0/2ibRp/REDACTED/v0NYeQflzC/74tJ/jkj7DH/REDACTED/REDACTED/IhYBph6PCAbv/a0FSs1OI9Wu8xK7kaIy2OgSIuHT/REDACTED/REDACTED/REDACTED/PXXZmByAew71JuEQ/REDACTED/geuAq7j/REDACTED/4fFozaLu/REDACTED/REDACTED/REDACTED/6lEMfFt58v8CAAD//7sJL1QAAAAGSURBVAMAYlBiCWXmy9cAAAAASUVORK5CYII=",
  "detail": "original"
}
```

> AGENT

The page rendered correctly in Chrome: the standalone route shows the leaderboard panel, hides the title/HUD chrome, and has no page errors. I saw one generic 404 in the console, so I’m identifying it before I call verification done.

> TOOL

tool_use js
id: call_7KZON2zTtfCgbraDvAd2TSQK
```json
{
  "title": "Identify 404 and Back behavior",
  "timeout_ms": 60000,
  "code": "var playwrightMod3 = await import('playwright');\nvar chromeBrowser2 = await playwrightMod3.chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });\nvar chromePage2 = await chromeBrowser2.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });\nvar failedResponses = [];\nvar pageErrors3 = [];\nchromePage2.on('response', (response) => {\n  if (response.status() >= 400) failedResponses.push({ url: response.url(), status: response.status() });\n});\nchromePage2.on('pageerror', (error) => pageErrors3.push(error.message));\nawait chromePage2.goto('http://127.0.0.1:5173/leaderboard', { waitUntil: 'domcontentloaded' });\nawait chromePage2.waitForSelector('.leaderboard.is-board:not(.hidden)', { timeout: 10000 });\nawait chromePage2.locator('[data-lb-back]').click();\nawait chromePage2.waitForURL('http://127.0.0.1:5173/', { timeout: 10000 });\nawait chromePage2.waitForSelector('#title-screen:not(.hidden)', { timeout: 10000 });\nvar backState = await chromePage2.evaluate(() => ({\n  pathname: window.location.pathname,\n  titleVisible: !document.getElementById('title-screen')?.classList.contains('hidden'),\n  leaderboardVisible: !!document.querySelector('.leaderboard:not(.hidden)'),\n  bodyClass: document.body.className,\n}));\nawait chromeBrowser2.close();\nnodeRepl.write(JSON.stringify({ failedResponses, pageErrors: pageErrors3, backState }, null, 2));"
}
```

> TOOL

tool_result
id: call_7KZON2zTtfCgbraDvAd2TSQK
```
Wall time: 2.9602 seconds
Output:
[{"type":"text","text":"{\n  \"failedResponses\": [],\n  \"pageErrors\": [],\n  \"backState\": {\n    \"pathname\": \"/\",\n    \"titleVisible\": true,\n    \"leaderboardVisible\": false,\n    \"bodyClass\": \"tv-on title-up\"\n  }\n}"}]
```

> AGENT

The follow-up browser pass is clean: no failed responses this time, no page errors, and the Back button returns from `/leaderboard` to `/` with the title screen visible again. I’m doing final status cleanup now, including stopping the dev server.

> TOOL

tool_use exec_command
id: call_ziHrI301iG6a03BPr7nEZis3
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_NVlDUOLruqFvnAdfGAn99fVj
```json
{
  "cmd": "git diff -- src/main.js src/style.css && git diff --no-index /dev/null vercel.json || true",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result
id: call_ziHrI301iG6a03BPr7nEZis3
```
Chunk ID: a7b6a3
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 30
Output:
## codex/leaderboard-route...origin/codex/leaderboard-route
 M src/main.js
 M src/style.css
?? .codex/
?? vercel.json

```

> TOOL

tool_result
id: call_NVlDUOLruqFvnAdfGAn99fVj
```
Chunk ID: 25f286
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 604
Output:
diff --git a/src/main.js b/src/main.js
index bfce42d..a606ca4 100644
--- a/src/main.js
+++ b/src/main.js
@@ -114,6 +114,8 @@ if (bgm && audioPanel && audioToggle && audioMute && audioVolume) {
 
 const params = new URLSearchParams(location.search);
 const requestedView = params.get("view");
+const normalizedPath = location.pathname.replace(/\/+$/, "") || "/";
+const isLeaderboardRoute = normalizedPath === "/leaderboard";
 
 function normalizeEndOutcome(value) {
   const v = String(value || "").trim().toLowerCase();
@@ -163,6 +165,7 @@ let level2Done = jumpToLevel3;
 
 function startNewGame() {
   const cleanUrl = new URL(window.location.href);
+  cleanUrl.pathname = "/";
   cleanUrl.search = "";
   cleanUrl.hash = "";
   window.location.assign(cleanUrl.href);
@@ -231,6 +234,10 @@ const titleLeaderboardPanel = createLeaderboardPanel({
 function closeTitleLeaderboard() {
   titleLeaderboardRequest += 1;
   titleLeaderboardPanel.hide();
+  if (isLeaderboardRoute) {
+    startNewGame();
+    return;
+  }
   const resume = resumeTitleAfterLeaderboard;
   resumeTitleAfterLeaderboard = null;
   resume?.();
@@ -268,7 +275,12 @@ const titleScreen = createTitleScreen({
   },
   onStart: () => planetView.setLandingMarkerHold(false),
 });
-if (!requestedView && !params.get("level") && !endShortcut) titleScreen.show();
+if (isLeaderboardRoute) {
+  document.body.classList.add("leaderboard-route");
+  showTitleLeaderboard();
+} else if (!requestedView && !params.get("level") && !endShortcut) {
+  titleScreen.show();
+}
 
 // ---------- fade transition ----------
 const fade = document.getElementById("fade");
diff --git a/src/style.css b/src/style.css
index 09b0a2a..62f9e85 100644
--- a/src/style.css
+++ b/src/style.css
@@ -98,6 […]

> TOOL

tool_use write_stdin
id: call_39xCKqoaI9axtWMiW9WZcxP6
```json
{
  "session_id": 65391,
  "chars": "\u0003",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_39xCKqoaI9axtWMiW9WZcxP6
```
Chunk ID: 3a505b
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 1
Output:
^C
```

> AGENT

Because this is trail work, I’m going to commit and push the scoped implementation so the trail actually has the code checkpoint attached. I’ll stage only `src/main.js`, `src/style.css`, and `vercel.json`; the existing untracked `.codex/` directory stays out of it.

> TOOL

tool_use exec_command
id: call_ARUz3kqxhEzRrAdcAFOCNReD
```json
{
  "cmd": "git add src/main.js src/style.css vercel.json && git diff --cached --stat && git diff --cached --name-only",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_ARUz3kqxhEzRrAdcAFOCNReD
```
Chunk ID: f930ec
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 44
Output:
 src/main.js   | 14 +++++++++++++-
 src/style.css |  4 ++++
 vercel.json   |  6 ++++++
 3 files changed, 23 insertions(+), 1 deletion(-)
src/main.js
src/style.css
vercel.json

```

> AGENT

The staged set is exactly the route bootstrap, chrome-hiding CSS, and Vercel rewrite. I’m committing and pushing that branch now.

> TOOL

tool_use exec_command
id: call_Y2ExT7ZACYwZeUJRGchRdYhI
```json
{
  "cmd": "git commit -m \"Render leaderboard route\" && git push origin codex/leaderboard-route",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result
id: call_Y2ExT7ZACYwZeUJRGchRdYhI
```
Chunk ID: da6710
Wall time: 11.6635 seconds
Process exited with code 0
Original token count: 85
Output:
[codex/leaderboard-route 35cdcfb] Render leaderboard route
 3 files changed, 23 insertions(+), 1 deletion(-)
 create mode 100644 vercel.json
[entire] Pushing entire/checkpoints/v1 to origin.... done
To https://github.com/blackgirlbytes/planetfall-seed-signalkit.git
   55eea2b..35cdcfb  codex/leaderboard-route -> codex/leaderboard-route

```

> AGENT

Commit and push succeeded, including the Entire checkpoint push. I’m doing one final status check so the close-out is precise.

> TOOL

tool_use exec_command
id: call_zkNySd9WQIIPKdeWjy7GPC63
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_Ssio3PD8RiOlSGMAd8mv8tok
```json
{
  "cmd": "git log -1 --oneline",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_FDM8itI6lmBsxnGPp1sn80OU
```json
{
  "cmd": "entire trail show",
  "workdir": "/home/<USER>/Documents/work/planetfall-seed-signalkit",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result
id: call_zkNySd9WQIIPKdeWjy7GPC63
```
Chunk ID: e2e437
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 18
Output:
## codex/leaderboard-route...origin/codex/leaderboard-route
?? .codex/

```

> TOOL

tool_result
id: call_Ssio3PD8RiOlSGMAd8mv8tok
```
Chunk ID: e3807d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 9
Output:
35cdcfb Render leaderboard route

```

> TOOL

tool_result
id: call_FDM8itI6lmBsxnGPp1sn80OU
```
Chunk ID: 3c1ab3
Wall time: 0.8453 seconds
Process exited with code 0
Original token count: 70
Output:
Trail: Render leaderboard at /leaderboard
  Number:  2
  ID:      019ee0a3-af9a-74e7-af75-00d0f1e20b66
  Branch:  codex/leaderboard-route
  Base:    main
  Status:  open
  Author:  blackgirlbytes
  Phase:   planning
  Created: 2026-06-19T16:08:03Z
  Updated: 2026-06-19T16:08:03Z

```

> AGENT

Executed the trail and pushed it.

`/leaderboard` now opens the existing leaderboard board directly, hides the normal HUD/title chrome, and the Back button returns to `/`. I also added `vercel.json` rewrites so direct production hits to `/leaderboard` serve the SPA entry.

Changed:
- [src/main.js](/home/<USER>/Documents/work/planetfall-seed-signalkit/src/main.js)
- [src/style.css](/home/<USER>/Documents/work/planetfall-seed-signalkit/src/style.css)
- [vercel.json](/home/<USER>/Documents/work/planetfall-seed-signalkit/vercel.json)

Verified with `npm test`, `npm run build`, and a Chrome pass against `http://127.0.0.1:5173/leaderboard`. Committed and pushed as `35cdcfb Render leaderboard route` on `codex/leaderboard-route`. The existing untracked `.codex/` directory is still untouched.

::git-stage{cwd="/home/<USER>/Documents/work/planetfall-seed-signalkit"}
::git-commit{cwd="/home/<USER>/Documents/work/planetfall-seed-signalkit"}
::git-push{cwd="/home/<USER>/Documents/work/planetfall-seed-signalkit" branch="codex/leaderboard-route"}