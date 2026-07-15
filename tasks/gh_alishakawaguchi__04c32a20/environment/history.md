> DEVELOPER

lets fix this issue https://github.com/entireio/skills/issues/6

> AGENT

I’m going to inspect the repo and pull in the GitHub issue details so we can fix the right thing end to end. After that I’ll trace the affected files, make the change, and verify it locally.

> TOOL

tool_use exec_command
id: call_I0XZLX6wH00DuJkZE6eF9iNA
```json
{
  "cmd": "pwd && rg --files",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_NPYx7Ycd8vdb3SXXNAHUkI5X
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_LoFBDfT8yM7jl8DdUkRoEu6G
```json
{
  "cmd": "git remote -v",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_oFHodXP9oLclsg88lfsmctUP
```json
{
  "cmd": "sed -n '1,200p' /Users/rizel/.agents/skills/entire/skills/search/SKILL.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 6000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_I0XZLX6wH00DuJkZE6eF9iNA
```
Chunk ID: 669552
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 51
Output:
/Users/rizel/Documents/work/skills
skills/what-happened/SKILL.md
skills/session-handoff/SKILL.md
skills/search/SKILL.md
skills/explain/SKILL.md
package.json
TUTORIAL.md
README.md
gemini-extension.json

```

> TOOL

tool_result
id: call_NPYx7Ycd8vdb3SXXNAHUkI5X
```
Chunk ID: 5243aa
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 10
Output:
## main...origin/main
?? TUTORIAL.md

```

> TOOL

tool_result
id: call_LoFBDfT8yM7jl8DdUkRoEu6G
```
Chunk ID: 30e4d5
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 27
Output:
origin	https://github.com/entireio/skills.git (fetch)
origin	https://github.com/entireio/skills.git (push)

```

> TOOL

tool_result
id: call_oFHodXP9oLclsg88lfsmctUP
```
Chunk ID: 348113
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 682
Output:
---
description: Use when the user wants to find prior work, checkpoints, or agent conversations by topic, repo, branch, author, or recent time window
---

# Search Checkpoints

Use `entire search` to find relevant checkpoints before guessing from memory.

## Response Format

Begin the first response to this skill invocation with the line:

`Entire Search:`

followed by a blank line, then the content.

- Apply the header to the **first response of the invocation only.** Do not re-print it on follow-up turns within the same invocation (e.g. after the user answers a clarifying question).
- Do **not** include the header on error or early-exit responses (e.g. "Entire CLI not installed", "authentication required", "no matches"). The header's presence should signal that the skill ran and produced real output.

## When to Use

- The user asks things like "have we done this before?", "search past work", "find the previous implementation", or "look for checkpoints about X"
- You need prior context from another branch, repo, author, or recent time period
- You want likely matches first, then a deeper transcript […]

> AGENT

I’ve confirmed the repo shape and there’s an untracked [TUTORIAL.md](/Users/rizel/Documents/work/skills/TUTORIAL.md) that I’ll leave alone. Next I’m pulling the issue details and reading the relevant skill files so we can patch the exact behavior the issue describes.

> TOOL

tool_use exec_command
id: call_cFw2MuqKlqQjPbx7B5HsT79l
```json
{
  "cmd": "sed -n '1,240p' README.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 8000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_gq1qCbMsUY8gREi1RW1hCfat
```json
{
  "cmd": "sed -n '1,240p' package.json",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_ItTvyJqWhAyHpXwNfhSLjECF
```json
{
  "cmd": "sed -n '1,240p' skills/what-happened/SKILL.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_oXAMBfUDzHJQUGxWl0zVZ4B2
```json
{
  "cmd": "sed -n '1,240p' skills/explain/SKILL.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_cFw2MuqKlqQjPbx7B5HsT79l
```
Chunk ID: 1037b3
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1422
Output:
# Skills

Cross-agent skills and commands powered by Entire.

## Skills

### `session-handoff`

Reads Entire session metadata and helps move work from one agent to another without making the user reconstruct the context manually.

Current behavior:

- auto-detects the most recent session from `.git/entire-sessions/`
- reads the raw transcript at the path stored in session metadata
- produces a structured compaction summary (Task Overview, Current State, Important Discoveries, Next Steps, Context to Preserve) instead of dumping raw transcript lines
- surfaces unanswered questions from the previous agent for the user to answer
- supports checkpoint handoff via `entire explain --checkpoint <id> --full --no-pager`
- falls back to `entire explain --checkpoint <id> --raw-transcript --no-pager` if full output is unavailable
- resolves checkpoints from: local `entire/checkpoints/v1` branch, `.entire/settings.json` `checkpoint_remote`, or nearby local clone
- filters sessions by agent name (e.g. "codex", "gemini") when mentioned

### `explain`

Traces source code back to the original conversation where it was created. Use `/explain` with a function, file, or line of code to understand _why_ it exists.

Current behavior:

- identifies the commit that introduced […]

> TOOL

tool_result
id: call_gq1qCbMsUY8gREi1RW1hCfat
```
Chunk ID: f2400a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 27
Output:
{
  "name": "skills",
  "version": "0.3.0",
  "type": "module",
  "main": ".opencode/plugins/entire.js"
}

```

> TOOL

tool_result
id: call_ItTvyJqWhAyHpXwNfhSLjECF
```
Chunk ID: e0979c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2982
Output:
---
name: What Happened
description: >
  Explain why code looks the way it does by tracing the latest change for a file
  range or pasted snippet through `git blame` and deduplicated `entire explain`
  lookups. Use when the user asks what happened, says "tell me why" about a code
  block, is confused about a section of code, asks "wtf is going on", "why is
  this like this", "why was this changed", or wants provenance for a specific
  file block.
---

# What Happened

Use this skill when the user wants a provenance-focused explanation for a code block.

Supported inputs:

- `path:line`
- `path:start-end`
- `path` plus a pasted code snippet from that file

If the user asks a vague provenance question without a file path, line range, or pasted
snippet, ask for the target code and stop without running commands or using the header.

## Goal

Find the most recent change blocks matching the user's target lines, list the matching
commit hashes and checkpoint state, then summarize why each block was changed using the
best available context. When checkpoint-backed context […]

> TOOL

tool_result
id: call_oXAMBfUDzHJQUGxWl0zVZ4B2
```
Chunk ID: a2a0c7
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 543
Output:
---
description: Explains the intent behind source code by finding original session transcripts. Use /explain with a function, file, or line of code to understand why it exists.
argument-hint: <function, file, or line>
---

# Explain Intent

Explain the intent behind source code by tracing it back to the original conversation where it was created. Works with:

- **Functions** — Why does this function exist? What problem was it solving?
- **Files** — What's the purpose of this file? What requirements drove its creation?
- **Line changes** — Why was this specific line added or modified?

## Response Format

Begin the first response to this skill invocation with the line:

`Entire Explain:`

followed by a blank line, then the content.

- Apply the header to the **first response of the invocation only.** Do not re-print it on follow-up turns within the same invocation (e.g. after the user answers a clarifying question).
- Do **not** include the header on error or early-exit responses (e.g. "Entire CLI is required but not installed", "this file is not tracked by git", "no session […]

> AGENT

The issue is clear now: clone-based installers only see one discoverable skill from this repo, and the likely culprit is the repository layout and how skill metadata is exposed. I’m checking the install surface the repo presents today against what flat auto-discovery tools usually expect, then I’ll patch the structure with the smallest compatible change.

> TOOL

tool_use exec_command
id: call_qyoAfSyYEmHBIQhI3MKmJYGx
```json
{
  "cmd": "find . -maxdepth 3 -type f | sort",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_Q8m0VPQl7Cyq2BCutdA3DDJV
```json
{
  "cmd": "find skills -maxdepth 2 -type f -name 'SKILL.md' -print -exec sh -c 'printf \"\\n--- %s ---\\n\" \"$1\"; sed -n \"1,40p\" \"$1\"' _ {} \\;",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 16000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_WCrjTnLBOcON0SHwLTWKB3Kq
```json
{
  "cmd": "sed -n '1,200p' gemini-extension.json",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 6000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_qyoAfSyYEmHBIQhI3MKmJYGx
```
Chunk ID: 5ae061
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 774
Output:
./.agents/plugins/marketplace.json
./.claude-plugin/marketplace.json
./.claude-plugin/plugin.json
./.claude/agents/entire-search.md
./.claude/settings.json
./.codex-plugin/plugin.json
./.codex/agents/entire-search.toml
./.codex/config.toml
./.codex/hooks.json
./.cursor-plugin/plugin.json
./.entire/.gitignore
./.entire/logs/entire.log
./.entire/settings.json
./.entire/tmp/pre-prompt-019da6bc-e9c8-7673-a95a-389290b40f0d.json
./.entire/tmp/pre-prompt-019da6bd-d6a9-7d21-923e-67d4b3e67e51.json
./.entire/tmp/pre-prompt-019da818-4448-77d0-ba6d-42f4a80a8fd1.json
./.entire/tmp/pre-prompt-019da819-9946-7040-a59c-7671e36ed4d8.json
./.entire/tmp/pre-prompt-019dd2de-e09a-7303-b360-73ccc99462f7.json
./.entire/tmp/pre-prompt-019dd2de-e4a5-7c12-857c-a116a6b4b86c.json
./.entire/tmp/pre-prompt-019dd445-c84a-7533-8a33-70ac5203b315.json
./.entire/tmp/pre-prompt-019dd491-17b4-71d0-b57f-8d1beac09a21.json
./.entire/tmp/pre-prompt-019dd4b9-496d-7581-a780-16f20aecff69.json
./.entire/tmp/pre-prompt-019dd4b9-59d8-7770-9ada-92bf6af154e8.json
./.git/FETCH_HEAD
./.git/HEAD
./.git/ORIG_HEAD
./.git/config
./.git/description
./.git/entire-sessions/019dd2de-aa63-7092-b57e-dd9e0ea6c5b8.json
./.git/entire-sessions/019dd2de-aa63-7092-b57e-dd9e0ea6c5b8.model
./.git/entire-sessions/019dd2de-e09a-7303-b360-73ccc99462f7.json
./.git/entire-sessions/019dd2de-e09a-7303-b360-73ccc99462f7.model
./.git/entire-sessions/019dd2de-e4a5-7c12-857c-a116a6b4b86c.json
./.git/entire-sessions/019dd2de-e4a5-7c12-857c-a116a6b4b86c.model
./.git/entire-sessions/019dd445-c84a-7533-8a33-70ac5203b315.json
./.git/entire-sessions/019dd445-c84a-7533-8a33-70ac5203b315.model
./.git/entire-sessions/019dd490-f7fb-7563-b789-5f5e6cc893fd.json
./.git/entire-sessions/019dd490-f7fb-7563-b789-5f5e6cc893fd.model
./.git/entire-sessions/019dd491-17b4-71d0-b57f-8d1beac09a21.json
./.git/entire-sessions/019dd491-17b4-71d0-b57f-8d1beac09a21.model
./.git/entire-sessions/019dd4b9-496d-7581-a780-16f20aecff69.json
./.git/entire-sessions/019dd4b9-496d-7581-a780-16f20aecff69.model
./.git/entire-sessions/019dd4b9-59d8-7770-9ada-92bf6af154e8.json
./.git/entire-sessions/019dd4b9-59d8-7770-9ada-92bf6af154e8.model
./.git/hooks/applypatch-msg.sample
./.git/hooks/commit-msg
./.git/hooks/commit-msg.sample
./.git/hooks/fsmonitor-watchman.sample
./.git/hooks/post-commit
./.git/hooks/post-rewrite
./.git/hooks/post-update.sample
./.git/hooks/pre-applypatch.sample
./.git/hooks/pre-commit.sample
./.git/hooks/pre-merge-commit.sample
./.git/hooks/pre-push
./.git/hooks/pre-push.sample
./.git/hooks/pre-rebase.sample
./.git/hooks/pre-receive.sample
./.git/hooks/prepare-commit-msg
./.git/hooks/prepare-commit-msg.sample
./.git/hooks/push-to-checkout.sample
./.git/hooks/sendemail-validate.sample
./.git/hooks/update.sample
./.git/index
./.git/info/exclude
./.git/logs/HEAD
./.git/packed-refs
./.git/shallow
./.gitignore
./.opencode/INSTALL.md
./.opencode/plugins/entire.js
./README.md
./TUTORIAL.md
./gemini-extension.json
./package.json
./skills/explain/SKILL.md
./skills/search/SKILL.md
./skills/session-handoff/SKILL.md
./skills/what-happened/SKILL.md

```

> TOOL

tool_result
id: call_Q8m0VPQl7Cyq2BCutdA3DDJV
```
Chunk ID: 86953c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2049
Output:
skills/explain/SKILL.md

--- skills/explain/SKILL.md ---
---
description: Explains the intent behind source code by finding original session transcripts. Use /explain with a function, file, or line of code to understand why it exists.
argument-hint: <function, file, or line>
---

# Explain Intent

Explain the intent behind source code by tracing it back to the original conversation where it was created. Works with:

- **Functions** — Why does this function exist? What problem was it solving?
- **Files** — What's the purpose of this file? What requirements drove its creation?
- **Line changes** — Why was this specific line added or modified?

## Response Format

Begin the first response to this skill invocation with the line:

`Entire Explain:`

followed by a blank line, then the content.

- Apply the header to the **first response of the invocation only.** Do not re-print it on follow-up turns within the same invocation (e.g. after the user answers a clarifying question).
- Do **not** include the header on error or early-exit responses (e.g. "Entire CLI is required but not installed", "this file is not tracked […]

> TOOL

tool_result
id: call_WCrjTnLBOcON0SHwLTWKB3Kq
```
Chunk ID: c4b92d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 29
Output:
{
  "name": "entire",
  "description": "Cross-agent skills and commands powered by Entire.",
  "version": "0.3.0"
}

```

> AGENT

I’ve narrowed the likely failure mode: `what-happened` is the only skill that currently declares an explicit frontmatter `name`, while the others only have `description`. I’m reproducing that against the actual `skills` installer now so we can confirm before editing anything.

> TOOL

tool_use exec_command
id: call_urHcZ3lCGxrWbEEsbrdBXATF
```json
{
  "cmd": "npx -y skills@1.5.2 add https://github.com/entireio/skills --dry-run",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000,
  "tty": false
}
```

> TOOL

tool_use exec_command
id: call_cI7TLBvtDXK5nqKmWkXqjnps
```json
{
  "cmd": "npx -y skills@1.5.2 --help",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 8000,
  "yield_time_ms": 1000,
  "tty": false
}
```

> TOOL

tool_result
id: call_urHcZ3lCGxrWbEEsbrdBXATF
```
Chunk ID: 2505f1
Wall time: 1.0012 seconds
Process running with session ID 80697
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_cI7TLBvtDXK5nqKmWkXqjnps
```
Chunk ID: e2d5d7
Wall time: 1.0019 seconds
Process running with session ID 57878
Original token count: 0
Output:

```

> TOOL

tool_use write_stdin
id: call_covGauzaN7zf83BLkszDBM3z
```json
{
  "session_id": 80697,
  "chars": "",
  "yield_time_ms": 1500,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use write_stdin
id: call_2ChksSbCRlOPkr4HX0hFyLLw
```json
{
  "session_id": 57878,
  "chars": "",
  "yield_time_ms": 1500,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_covGauzaN7zf83BLkszDBM3z
```
Chunk ID: 7b6a39
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 700
Output:

[38;5;250m███████╗██╗  ██╗██╗██╗     ██╗     ███████╗[0m
[38;5;248m██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝[0m
[38;5;245m███████╗█████╔╝ ██║██║     ██║     ███████╗[0m
[38;5;243m╚════██║██╔═██╗ ██║██║     ██║     ╚════██║[0m
[38;5;240m███████║██║  ██╗██║███████╗███████╗███████║[0m
[38;5;238m╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝[0m

┌   skills 
│
│  Tip: use the --yes (-y) and --global (-g) flags to install without prompts.
[?25l│
◇  Source: https://github.com/entireio/skills.git
[?25h[?25l│
◒  Cloning repository[999D[J◐  Cloning repository[999D[J◓  Cloning repository[999D[J◑  Cloning repository[999D[J◇  Repository cloned
[?25h[?25l│
[999D[J◇  Found 1 skill
[?25h│
●  Skill: What Happened
│
│  Explain why code looks the way it does by tracing the latest change for a file range or pasted snippet through `git blame` and deduplicated `entire explain` lookups. Use when the user asks what happened, says "tell me why" about a code block, is confused about a section of code, asks "wtf is going on", "why is this like this", "why was this changed", or wants provenance for a specific file block.
[?25l│
[999D[J◇  53 agents
[?25h◆  Which agents do you want to install to?
│
│  ── Universal (.agents/skills) ── always included ────────────
│    • Amp
│    • Antigravity
│    • Cline
│    • Codex
│    • Cursor
│    • Deep Agents
│ […]

> TOOL

tool_result
id: call_2ChksSbCRlOPkr4HX0hFyLLw
```
Chunk ID: 84eb47
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1076
Output:

[1mUsage:[0m skills <command> [options]

[1mManage Skills:[0m
  add <package>        Add a skill package (alias: a)
                       e.g. vercel-labs/agent-skills
                            https://github.com/vercel-labs/agent-skills
  remove [skills]      Remove installed skills
  list, ls             List installed skills
  find [query]         Search for skills interactively

[1mUpdates:[0m
  update [skills...]   Update skills to latest versions (alias: upgrade)

[1mUpdate Options:[0m
  -g, --global           Update global skills only
  -p, --project          Update project skills only
  -y, --yes              Skip scope prompt (auto-detect: project if in a project, else global)

[1mProject:[0m
  experimental_install Restore skills from skills-lock.json
  init [name]          Initialize a skill (creates <name>/SKILL.md or ./SKILL.md)
  experimental_sync    Sync skills from node_modules into agent directories

[1mAdd Options:[0m
  -g, --global           Install skill globally (user-level) instead of project-level
  -a, --agent <agents>   Specify agents to install to (use '*' for all agents)
  -s, --skill <skills>   Specify skill names to install (use '*' for all skills)
  -l, --list             List available skills in the repository without installing
  -y, --yes              Skip confirmation prompts
  --copy                 Copy files instead of symlinking to agent directories
  --all                  Shorthand for --skill '*' --agent '*' -y
  --full-depth           Search all subdirectories even when a root SKILL.md exists

[1mRemove Options:[0m
  -g, --global           Remove from global […]

> AGENT

The reproduction matches the issue exactly on `skills@1.5.2`: the installer reports “Found 1 skill” and only surfaces `What Happened`. I’m inspecting the installer’s discovery logic now to confirm whether the missing `name` metadata is the actual discriminator before I patch the repo.

> TOOL

tool_use exec_command
id: call_OiUC8SXlzBFMYbaKLmbw7qVy
```json
{
  "cmd": "tmpdir=$(mktemp -d) && cd \"$tmpdir\" && npm pack skills@1.5.2 >/dev/null && tar -xzf skills-1.5.2.tgz && rg -n \"name:|frontmatter|gray-matter|SKILL.md|Found 1 skill|Found .* skill|description\" package -S",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 16000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_rDnVJDZ5VXAKMyRMdp079OSJ
```json
{
  "cmd": "npx -y skills@1.5.2 add https://github.com/entireio/skills --list --yes",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_OiUC8SXlzBFMYbaKLmbw7qVy
```
Chunk ID: ee3524
Wall time: 0.0409 seconds
Process exited with code 0
Original token count: 3114
Output:
npm notice
npm notice 📦  skills@1.5.2
npm notice Tarball Contents
npm notice 20.1kB README.md
npm notice 6.6kB ThirdPartyNoticeText.txt
npm notice 305B bin/cli.mjs
npm notice 47.1kB dist/_chunks/libs/@clack/core.mjs
npm notice 16.4kB dist/_chunks/libs/@clack/prompts.mjs
npm notice 15.8kB dist/_chunks/libs/@kwsites/file-exists.mjs
npm notice 841B dist/_chunks/libs/@kwsites/promise-deferred.mjs
npm notice 115.9kB dist/_chunks/libs/simple-git.mjs
npm notice 805B dist/_chunks/libs/xdg-basedir.mjs
npm notice 1.5kB dist/_chunks/rolldown-runtime.mjs
npm notice 11B dist/cli.d.mts
npm notice 179.7kB dist/cli.mjs
npm notice 2.7kB package.json
npm notice Tarball Details
npm notice name: skills
npm notice version: 1.5.2
npm notice filename: skills-1.5.2.tgz
npm notice package size: 95.0 kB
npm notice unpacked size: 407.6 kB
npm notice shasum: 8ca0d916cf9468751bac1585dbb0cd46467aa1f2
npm notice integrity: sha512-ERMYM+UpIYi8+[...]RKC1PRhqeyZyA==
npm notice total files: 13
npm notice
package/package.json:4:  "description": "The open agent skills ecosystem",
package/README.md:101:| `npx skills init [name]`     | Create a new SKILL.md template                |
package/README.md:160:# Create SKILL.md in current directory
package/README.md:210:Agent skills are reusable instruction sets that extend your coding agent's capabilities. They're defined in `SKILL.md`
package/README.md:211:files with YAML frontmatter containing a `name` and `description`.
package/README.md:285:>   "resources": ["skill://.kiro/skills/**/SKILL.md"]
package/README.md:294:Skills are directories containing a `SKILL.md` file with YAML frontmatter:
package/README.md:298:name: my-skill
package/README.md:299:description: What this skill does and when to use […]

> TOOL

tool_result
id: call_rDnVJDZ5VXAKMyRMdp079OSJ
```
Chunk ID: efe9a9
Wall time: 0.6088 seconds
Process exited with code 0
Original token count: 419
Output:

[38;5;250m███████╗██╗  ██╗██╗██╗     ██╗     ███████╗[0m
[38;5;248m██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝[0m
[38;5;245m███████╗█████╔╝ ██║██║     ██║     ███████╗[0m
[38;5;243m╚════██║██╔═██╗ ██║██║     ██║     ╚════██║[0m
[38;5;240m███████║██║  ██╗██║███████╗███████╗███████║[0m
[38;5;238m╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝[0m

┌   skills 
│
│  Tip: use the --yes (-y) and --global (-g) flags to install without prompts.
[?25l│
◇  Source: https://github.com/entireio/skills.git
[?25h[?25l│
◒  Cloning repository[999D[J◐  Cloning repository[999D[J◓  Cloning repository[999D[J◑  Cloning repository[999D[J◇  Repository cloned
[?25h[?25l│
[999D[J◇  Found 1 skill
[?25h
│
◇  Available Skills
│
│    What Happened
│
│      Explain why code looks the way it does by tracing the latest change for a file range or pasted snippet through `git blame` and deduplicated `entire explain` lookups. Use when the user asks what happened, says "tell me why" about a code block, is confused about a section of code, asks "wtf is going on", "why is this like this", "why was this changed", or wants provenance for a specific file block.

│
└  Use --skill <name> to install specific skills


```

> AGENT

The installer source confirms it: it ignores any `SKILL.md` whose frontmatter does not include both `name` and `description`. That means the fix is structural rather than behavioral, so I’m adding explicit skill names to the missing files and then I’ll rerun the exact installer repro.

> TOOL

tool_use exec_command
id: call_zQNdhB5Hq5ZJOZvQxcIEpDgN
```json
{
  "cmd": "rg -n \"session-handoff|what-happened|Entire Search|Entire Explain|name:\" README.md skills .codex .claude .agents gemini-extension.json .cursor-plugin .codex-plugin .claude-plugin .opencode -S",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_2rD8DQZwDnRrt2icevb1pRcW
```json
{
  "cmd": "git ls-files --stage skills/explain/SKILL.md skills/search/SKILL.md skills/session-handoff/SKILL.md skills/what-happened/SKILL.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_zQNdhB5Hq5ZJOZvQxcIEpDgN
```
Chunk ID: 1d8d07
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 238
Output:
README.md:7:### `session-handoff`
README.md:33:### `what-happened`
README.md:73:npx skills add https://github.com/entireio/skills --skill session-handoff
.opencode/INSTALL.md:31:Verify by asking: "Use the `session-handoff` skill."
.cursor-plugin/plugin.json:12:  "keywords": ["entire", "session-handoff", "what-happened", "handoff", "agent-workflows", "skills"],
.claude-plugin/plugin.json:15:    "what-happened",
skills/what-happened/SKILL.md:2:name: What Happened
.codex-plugin/plugin.json:14:    "session-handoff",
.codex-plugin/plugin.json:15:    "what-happened",
.claude/agents/entire-search.md:2:name: entire-search
skills/explain/SKILL.md:18:`Entire Explain:`
skills/search/SKILL.md:13:`Entire Search:`
skills/search/SKILL.md:26:Do not use this for the current active session. Use `session-handoff` for that.
skills/search/SKILL.md:69:- If the user really wants the current session, switch to `session-handoff` instead of searching checkpoints

```

> TOOL

tool_result
id: call_2rD8DQZwDnRrt2icevb1pRcW
```
Chunk ID: 4db38f
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 78
Output:
100644 c53f01aaf672b99a72cf1a3c4c3a275f86b73d24 0	skills/explain/SKILL.md
100644 b3b5c0d00e90bfedcc1354d04a5e05269c20b5df 0	skills/search/SKILL.md
100644 4b1d5b105d25f3fa5cb2ddd0f9d1253fa090b80d 0	skills/session-handoff/SKILL.md
100644 4507719c5c2c036daf5b753b18df0736edcedca7 0	skills/what-happened/SKILL.md

```

> AGENT

I’m making a very small patch: just the missing frontmatter fields that the installer requires for discovery. After that I’ll rerun the installer against the local checkout to prove it now sees all four skills.

> TOOL

tool_use exec_command
id: call_DNAX0FUZdHnZeSpTzJPhTUj0
```json
{
  "cmd": "npx -y skills@1.5.2 add /Users/rizel/Documents/work/skills --list --yes",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_twv1aeeTjhHDwisFq6Z7JcZU
```json
{
  "cmd": "git diff -- skills/explain/SKILL.md skills/search/SKILL.md skills/session-handoff/SKILL.md",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 8000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_DNAX0FUZdHnZeSpTzJPhTUj0
```
Chunk ID: 58375a
Wall time: 0.3615 seconds
Process exited with code 0
Original token count: 523
Output:

[38;5;250m███████╗██╗  ██╗██╗██╗     ██╗     ███████╗[0m
[38;5;248m██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝[0m
[38;5;245m███████╗█████╔╝ ██║██║     ██║     ███████╗[0m
[38;5;243m╚════██║██╔═██╗ ██║██║     ██║     ╚════██║[0m
[38;5;240m███████║██║  ██╗██║███████╗███████╗███████║[0m
[38;5;238m╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝[0m

┌   skills 
│
│  Tip: use the --yes (-y) and --global (-g) flags to install without prompts.
[?25l│
◇  Source: /Users/rizel/Documents/work/skills
[?25h[?25l│
◇  Local path validated
[?25h[?25l│
◇  Found 4 skills
[?25h
│
◇  Available Skills
│
│    explain
│
│      Explains the intent behind source code by finding original session transcripts. Use /explain with a function, file, or line of code to understand why it exists.
│
│    search
│
│      Use when the user wants to find prior work, checkpoints, or agent conversations by topic, repo, branch, author, or recent time window
│
│    session-handoff
│
│      Use when the user wants to continue work from one agent in another agent, inspect recent sessions, or summarize a saved session or checkpoint for handoff
│
│    What Happened
│
│      Explain why code looks the way it does by tracing the latest change for a file range or pasted snippet through `git blame` and deduplicated `entire explain` lookups. […]

> TOOL

tool_result
id: call_twv1aeeTjhHDwisFq6Z7JcZU
```
Chunk ID: 3e7139
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 517
Output:
diff --git a/skills/explain/SKILL.md b/skills/explain/SKILL.md
index c53f01a..2cab7a8 100644
--- a/skills/explain/SKILL.md
+++ b/skills/explain/SKILL.md
@@ -1,4 +1,5 @@
 ---
+name: explain
 description: Explains the intent behind source code by finding original session transcripts. Use /explain with a function, file, or line of code to understand why it exists.
 argument-hint: <function, file, or line>
 ---
@@ -30,4 +31,4 @@ followed by a blank line, then the content.
    - If the file is not tracked by git, stop and tell the user: "This file is not tracked by git, so I can't trace its history."
    - If git blame returns no useful result (e.g., the code is uncommitted), stop and tell the user: "This code hasn't been committed yet, so there's no history to trace."
 3. Use a Sonnet agent to read the session transcript via `entire explain --no-pager --commit COMMIT_SHA`.
-   - If the command fails or returns no transcript, stop and tell the user: "No session transcript was found for this commit. It may have been created outside of an Entire session (e.g., a manual commit)."
\ No newline at end of […]

> AGENT

The patch is behaving the way we wanted: the same installer version now reports `Found 4 skills` against this checkout. I’m doing one last quick sanity pass for diff cleanliness, then I’ll hand you the exact change and verification.

> TOOL

tool_use exec_command
id: call_YNJz9imSrP8wxGB4ORyhhYKy
```json
{
  "cmd": "git diff --check",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_use exec_command
id: call_nUShnvzfbhkgw1876xEsEx4k
```json
{
  "cmd": "git status --short",
  "workdir": "/Users/rizel/Documents/work/skills",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result
id: call_YNJz9imSrP8wxGB4ORyhhYKy
```
Chunk ID: eecbb5
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_nUShnvzfbhkgw1876xEsEx4k
```
Chunk ID: e5dc03
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 26
Output:
 M skills/explain/SKILL.md
 M skills/search/SKILL.md
 M skills/session-handoff/SKILL.md
?? TUTORIAL.md

```

> AGENT

The issue is fixed in this checkout by adding the missing `name` frontmatter to the three undiscoverable skills: [skills/explain/SKILL.md](/Users/rizel/Documents/work/skills/skills/explain/SKILL.md), [skills/search/SKILL.md](/Users/rizel/Documents/work/skills/skills/search/SKILL.md), and [skills/session-handoff/SKILL.md](/Users/rizel/Documents/work/skills/skills/session-handoff/SKILL.md). `skills@1.5.2` requires both `name` and `description` in `SKILL.md`, which is why only `what-happened` had been detected before.

I verified the repro locally with `npx -y skills@1.5.2 add /Users/rizel/Documents/work/skills --list --yes`, and it now reports `Found 4 skills` instead of `Found 1 skill`. `git diff --check` is clean. I left the untracked [TUTORIAL.md](/Users/rizel/Documents/work/skills/TUTORIAL.md) alone.