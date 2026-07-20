> DEVELOPER

some of the agent installs aren't working like cursor. can we update the repo to follow the smae skills install as this one /home/<USER>/Projects/cc-skills-golang

> AGENT

I'll explore both repos to understand the install patterns.

> TOOL

tool_use Bash
id: toolu_011McThZGAKwmnS5cUEkQgqo
```json
{
  "command": "ls -la /home/<USER>/Projects/skills /home/<USER>/Projects/cc-skills-golang",
  "description": "List both repos"
}
```

> TOOL

tool_result
id: toolu_011McThZGAKwmnS5cUEkQgqo
```
/home/<USER>/Projects/cc-skills-golang:
total 1800
drwxr-xr-x@ 16 alisha  staff     512 Apr 24 09:46 .
drwxr-xr-x@ 36 alisha  staff    1152 Apr 24 09:46 ..
drwxr-xr-x@  3 alisha  staff      96 Apr 24 09:46 .claude-plugin
drwxr-xr-x@  3 alisha  staff      96 Apr 24 09:46 .cursor-plugin
drwxr-xr-x@ 12 alisha  staff     384 Apr 24 09:46 .git
drwxr-xr-x@  5 alisha  staff     160 Apr 24 09:46 .github
-rw-r--r--@  1 alisha  staff      13 Apr 24 09:46 .gitignore
-rw-r--r--@  1 alisha  staff    1140 Apr 24 09:46 .markdownlint-cli2.jsonc
-rw-r--r--@  1 alisha  staff      26 Apr 24 09:46 .prettierrc
-rw-r--r--@  1 alisha  staff   43914 Apr 24 09:46 CLAUDE.md
-rw-r--r--@  1 alisha  staff  839120 Apr 24 09:46 EVALUATIONS.md
-rw-r--r--@  1 alisha  staff    1070 Apr 24 09:46 LICENSE
-rw-r--r--@  1 alisha  staff   10582 Apr 24 09:46 README.md
-rwxr-xr-x@  1 alisha  staff     950 Apr 24 09:46 clawhub-publish.sh
-rw-r--r--@  1 alisha  staff     123 Apr 24 09:46 gemini-extension.json
drwxr-xr-x@ 37 alisha  staff    1184 Apr 24 09:46 skills

/home/<USER>/Projects/skills:
total 40
drwxr-xr-x@ 17 alisha  staff   544 Apr 24 09:48 .
drwxr-xr-x@ 36 alisha  staff  1152 Apr 24 09:46 ..
drwxr-xr-x@  3 alisha  staff    96 Apr 10 10:35 .agents
drwxr-xr-x@  5 alisha  staff   160 Apr 10 12:53 .claude
drwxr-xr-x@  3 alisha  staff    96 Apr 10 13:31 .claude-plugin
drwxr-x---@ […]

> TOOL

tool_use Bash
id: toolu_01LEVgADSGj345R669K8Bqtu
```json
{
  "command": "ls -la /home/<USER>/Projects/cc-skills-golang/.claude-plugin /home/<USER>/Projects/cc-skills-golang/.cursor-plugin /home/<USER>/Projects/skills/.claude-plugin /home/<USER>/Projects/skills/.cursor-plugin",
  "description": "List plugin dirs in both repos"
}
```

> TOOL

tool_result
id: toolu_01LEVgADSGj345R669K8Bqtu
```
/home/<USER>/Projects/cc-skills-golang/.claude-plugin:
total 8
drwxr-xr-x@  3 alisha  staff   96 Apr 24 09:46 .
drwxr-xr-x@ 16 alisha  staff  512 Apr 24 09:46 ..
-rw-r--r--@  1 alisha  staff  643 Apr 24 09:46 plugin.json

/home/<USER>/Projects/cc-skills-golang/.cursor-plugin:
total 8
drwxr-xr-x@  3 alisha  staff   96 Apr 24 09:46 .
drwxr-xr-x@ 16 alisha  staff  512 Apr 24 09:46 ..
-rw-r--r--@  1 alisha  staff  657 Apr 24 09:46 plugin.json

/home/<USER>/Projects/skills/.claude-plugin:
total 8
drwxr-xr-x@  3 alisha  staff   96 Apr 10 13:31 .
drwxr-xr-x@ 17 alisha  staff  544 Apr 24 09:48 ..
-rw-r--r--@  1 alisha  staff  525 Apr 10 13:31 marketplace.json

/home/<USER>/Projects/skills/.cursor-plugin:
total 8
drwxr-xr-x@  3 alisha  staff   96 Apr 24 09:48 .
drwxr-xr-x@ 17 alisha  staff  544 Apr 24 09:48 ..
-rw-r--r--@  1 alisha  staff  438 Apr 24 09:48 plugin.json
```

> TOOL

tool_use Read
id: toolu_01WxC8gBkDGKfZMwCai5Bw6A
```json
{
  "file_path": "/home/<USER>/Projects/cc-skills-golang/.claude-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_01WxC8gBkDGKfZMwCai5Bw6A
```
1	{
2	    "name": "cc-skills-golang",
3	    "description": "AI Agent Skills for production-ready Go projects",
4	    "version": "1.2.5",
5	    "author": {
6	        "name": "Samuel Berthe",
7	        "email": "<REDACTED_EMAIL>"
8	    },
9	    "homepage": "https://github.com/samber/cc-skills-golang",
10	    "repository": "https://github.com/samber/cc-skills-golang",
11	    "license": "MIT",
12	    "keywords": [
13	        "claude-code",
14	        "claude-code-plugin",
15	        "plugin",
16	        "go",
17	        "golang",
18	        "ai-agent",
19	        "skills",
20	        "agentic",
21	        "engineering",
22	        "developer",
23	        "coding",
24	        "productivity"
25	    ]
26	}
```

> TOOL

tool_use Read
id: toolu_01Wbwp8FfgHHC6VYNxcqe5ka
```json
{
  "file_path": "/home/<USER>/Projects/cc-skills-golang/.cursor-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_01Wbwp8FfgHHC6VYNxcqe5ka
```
1	{
2	    "name": "cc-skills-golang",
3	    "displayName": "Skills for Golang",
4	    "description": "AI Agent Skills for production-ready Go projects",
5	    "version": "1.2.5",
6	    "author": {
7	        "name": "Samuel Berthe",
8	        "email": "<REDACTED_EMAIL>"
9	    },
10	    "homepage": "https://github.com/samber/cc-skills-golang",
11	    "repository": "https://github.com/samber/cc-skills-golang",
12	    "license": "MIT",
13	    "keywords": [
14	        "plugin",
15	        "go",
16	        "golang",
17	        "ai-agent",
18	        "skills",
19	        "agentic",
20	        "engineering",
21	        "developer",
22	        "coding",
23	        "productivity"
24	    ],
25	    "skills": "./skills/"
26	}
```

> TOOL

tool_use Read
id: toolu_01F9XKhG9qVHL3h11Wfg5Jia
```json
{
  "file_path": "/home/<USER>/Projects/skills/.claude-plugin/marketplace.json"
}
```

> TOOL

tool_result
id: toolu_01F9XKhG9qVHL3h11Wfg5Jia
```
1	{
2	  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
3	  "name": "entire-skills",
4	  "description": "Development marketplace for cross-agent skills and commands powered by Entire",
5	  "owner": {
6	    "name": "Entire Inc"
7	  },
8	  "plugins": [
9	    {
10	      "name": "entire",
11	      "description": "Cross-agent skills and commands powered by Entire",
12	      "version": "0.1.0",
13	      "source": "./plugins/entire",
14	      "category": "development",
15	      "author": {
16	        "name": "Entire Inc"
17	      }
18	    }
19	  ]
20	}
21	
```

> TOOL

tool_use Read
id: toolu_015tSLi6688pP8FkRbpazvGv
```json
{
  "file_path": "/home/<USER>/Projects/skills/.cursor-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_015tSLi6688pP8FkRbpazvGv
```
1	{
2	  "name": "entire",
3	  "displayName": "Entire",
4	  "description": "Cross-agent skills and commands powered by Entire.",
5	  "version": "0.1.0",
6	  "author": {
7	    "name": "Entire Inc"
8	  },
9	  "homepage": "https://github.com/entireio/skills",
10	  "repository": "https://github.com/entireio/skills",
11	  "license": "MIT",
12	  "keywords": ["entire", "session-handoff", "handoff", "agent-workflows", "skills"],
13	  "skills": "./plugins/entire/skills/"
14	}
15	
```

> TOOL

tool_use Read
id: toolu_01W5eZUhbv658zxj9uAm7H3e
```json
{
  "file_path": "/home/<USER>/Projects/skills/README.md"
}
```

> TOOL

tool_result
id: toolu_01W5eZUhbv658zxj9uAm7H3e
```
1	# Skills
2	
3	Cross-agent skills and commands powered by Entire.
4	
5	This repo is a shared skill collection for:
6	
7	- Codex
8	- Claude
9	- OpenCode
10	- Cursor
11	- Gemini
12	
13	## Skills
14	
15	### `session-handoff`
16	
17	Reads Entire session metadata and helps move work from one agent to another without making the user reconstruct the context manually.
18	
19	Current behavior:
20	
21	- auto-detects the most recent session from `.git/entire-sessions/`
22	- reads the raw transcript at the path stored in session metadata
23	- produces a structured compaction summary (Task Overview, Current State, Important Discoveries, Next Steps, Context to Preserve) instead of dumping raw transcript lines
24	- surfaces unanswered questions from the previous agent for the user to answer
25	- supports checkpoint handoff via `entire explain --checkpoint <id> --full --no-pager`
26	- falls back to `entire explain --checkpoint <id> --raw-transcript --no-pager` if full output is unavailable
27	- resolves checkpoints from: local `entire/checkpoints/v1` branch, `.entire/settings.json` `checkpoint_remote`, or nearby local clone
28	- filters sessions by agent name (e.g. "codex", "gemini") when mentioned
29	
30	### `explain`
31	
32	Traces source […]

> TOOL

tool_use Read
id: toolu_01P1QDmWnmwKFcyKRgej2j5R
```json
{
  "file_path": "/home/<USER>/Projects/cc-skills-golang/README.md"
}
```

> TOOL

tool_result
id: toolu_01P1QDmWnmwKFcyKRgej2j5R
```
1	# Agent Skills for production-ready Golang projects
2	
3	AI agent skills are reusable instruction sets that extend your coding assistant with domain-specific expertise, loaded on demand so they don't bloat your context. This repository covers **Go-specific** skills only (language, testing, security, observability, etc.); for dev workflow skills (git conventions, CI/CD, PR reviews) you'll want to add a separate skills plugin.
4	
5	For generic skills, please visit [cc-skills](https://github.com/samber/cc-skills).
6	
7	> [!IMPORTANT]
8	> Bootstrapped with Claude Code by distilling my Go project commits. **Edited, tested, reviewed and reworked by a human**.
9	>
10	> **No AI slop here.** AI-made skills are useless.
11	
12	<img width="1414" height="491" alt="image" src="https://github.com/user-attachments/assets/620b5835-c1ba-4ea9-bf47-2293b58b879e" />
13	
14	## 🚀 How to use
15	
16	**Install with [skills](https://skills.sh/) CLI** (universal, works with any [Agent Skills](https://agentskills.io)-compatible tool):
17	
18	```bash
19	npx skills add https://github.com/samber/cc-skills-golang --all
20	# or a single skill:
21	npx skills add https://github.com/samber/cc-skills-golang --skill golang-performance
22	```
23	
24	<!-- prettier-ignore-start -->
25	
26	<details>
27	<summary>Claude Code</summary>
28	
29	```bash
30	/plugin marketplace add samber/cc
31	/plugin install cc-skills-golang@samber
32	```
33	
34	</details>
35	
36	<details>
37	<summary>Openclaw</summary>
38	
39	Copy skills into […]

> TOOL

tool_use Bash
id: toolu_01QVWenPoAkaYGtxmu4XQoDZ
```json
{
  "command": "ls /home/<USER>/Projects/cc-skills-golang/skills/ | head -20 && echo \"---\" && ls /home/<USER>/Projects/skills/plugins/",
  "description": "Check skill directory structures"
}
```

> TOOL

tool_result
id: toolu_01QVWenPoAkaYGtxmu4XQoDZ
```
golang-benchmark
golang-cli
golang-code-style
golang-concurrency
golang-context
golang-continuous-integration
golang-data-structures
golang-database
golang-dependency-injection
golang-dependency-management
golang-design-patterns
golang-documentation
golang-error-handling
golang-grpc
golang-lint
golang-modernize
golang-naming
golang-observability
golang-performance
golang-popular-libraries
---
entire
```

> TOOL

tool_use Bash
id: toolu_01KWGkJbf69BCrWYfnYsAtMR
```json
{
  "command": "ls /home/<USER>/Projects/skills/plugins/entire/ && echo \"---\" && ls /home/<USER>/Projects/skills/plugins/entire/skills/ 2>/dev/null && echo \"---\" && find /home/<USER>/Projects/skills -maxdepth 4 -name \"*.json\" -o -name \"*.md\" | grep -v node_modules | grep -v \".git/\" | head -40",
  "description": "Check skill directory structures"
}
```

> TOOL

tool_result
id: toolu_01KWGkJbf69BCrWYfnYsAtMR
```
skills
---
explain
search
session-handoff
---
/home/<USER>/Projects/skills/gemini-extension.json
/home/<USER>/Projects/skills/README.md
/home/<USER>/Projects/skills/package.json
/home/<USER>/Projects/skills/GEMINI.md
/home/<USER>/Projects/skills/.cursor-plugin/plugin.json
/home/<USER>/Projects/skills/.opencode/INSTALL.md
/home/<USER>/Projects/skills/.claude/settings.json
/home/<USER>/Projects/skills/.claude/settings.local.json
/home/<USER>/Projects/skills/.codex/hooks.json
/home/<USER>/Projects/skills/.claude-plugin/marketplace.json
/home/<USER>/Projects/skills/.entire/settings.json
/home/<USER>/Projects/skills/.agents/plugins/marketplace.json
/home/<USER>/Projects/skills/.claude/agents/entire-search.md
/home/<USER>/Projects/skills/plugins/entire/.claude-plugin/plugin.json
/home/<USER>/Projects/skills/plugins/entire/.codex-plugin/plugin.json
/home/<USER>/Projects/skills/docs/superpowers/plans/2026-04-17-entire-skill-response-header.md
/home/<USER>/Projects/skills/docs/superpowers/specs/2026-04-17-entire-skill-response-header-design.md
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-ba833b9a-5a6d-4987-baa5-2f1dd001ad2e.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-3015d202-4959-4c66-9da5-a8eddaa630e7.json
/home/<USER>/Projects/skills/.entire/tmp/REDACTED.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-c5b3d2bd-c81b-487f-94a7-8fcb42d2abcb.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-c609b17b-6e60-4668-9859-8b5d93621f88.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-d74a0b14-40c3-4fa5-8888-153f902e94e7.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-95047199-69f0-49a5-9432-18cba428ecec.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-df990770-23b4-4652-a286-25ea441b647e.json
/home/<USER>/Projects/skills/.entire/tmp/pre-prompt-0953ba2a-3a92-48a0-884e-ce8f7ebbe8ba.json
```

> TOOL

tool_use Read
id: toolu_01Nwwr7f6aEsK6Zg5WnPn7g5
```json
{
  "file_path": "/home/<USER>/Projects/skills/plugins/entire/.claude-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_01Nwwr7f6aEsK6Zg5WnPn7g5
```
1	{
2	  "name": "entire",
3	  "version": "0.1.0",
4	  "description": "Cross-agent skills and commands powered by Entire",
5	  "author": {
6	    "name": "Entire Inc"
7	  },
8	  "homepage": "https://github.com/entireio/skills",
9	  "repository": "https://github.com/entireio/skills",
10	  "license": "MIT",
11	  "keywords": [
12	    "entire",
13	    "skills",
14	    "handoff",
15	    "agent-workflows",
16	    "plugins"
17	  ]
18	}
19	
```

> TOOL

tool_use Read
id: toolu_01FSwXMgs9mRU8DEwFP2KUDY
```json
{
  "file_path": "/home/<USER>/Projects/skills/gemini-extension.json"
}
```

> TOOL

tool_result
id: toolu_01FSwXMgs9mRU8DEwFP2KUDY
```
1	{
2	  "name": "entire",
3	  "description": "Cross-agent skills and commands powered by Entire.",
4	  "version": "0.1.0",
5	  "contextFileName": "GEMINI.md"
6	}
7	
```

> TOOL

tool_use Read
id: toolu_01UxtMVEWY6nJ1hMxMLZQJKs
```json
{
  "file_path": "/home/<USER>/Projects/cc-skills-golang/gemini-extension.json"
}
```

> TOOL

tool_result
id: toolu_01UxtMVEWY6nJ1hMxMLZQJKs
```
1	{
2	  "name": "cc-skills-golang",
3	  "version": "1.2.5",
4	  "description": "AI Agent Skills for production-ready Go projects"
5	}
```

> TOOL

tool_use Read
id: toolu_01Q6nERVSUmqqohUM5qq6bfL
```json
{
  "file_path": "/home/<USER>/Projects/skills/plugins/entire/.codex-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_01Q6nERVSUmqqohUM5qq6bfL
```
1	{
2	  "name": "entire",
3	  "version": "0.1.0",
4	  "description": "Cross-agent skills and commands powered by Entire.",
5	  "author": {
6	    "name": "Entire Inc",
7	    "url": "https://github.com/entireio"
8	  },
9	  "homepage": "https://github.com/entireio/skills",
10	  "repository": "https://github.com/entireio/skills",
11	  "license": "MIT",
12	  "keywords": [
13	    "entire",
14	    "session-handoff",
15	    "handoff",
16	    "agent-workflows",
17	    "skills"
18	  ],
19	  "skills": "./skills/",
20	  "interface": {
21	    "displayName": "Entire",
22	    "shortDescription": "Continue work across agents with session handoff",
23	    "developerName": "Entire Inc",
24	    "category": "Development",
25	    "capabilities": [
26	      "Interactive",
27	      "Write"
28	    ],
29	    "websiteURL": "https://github.com/entireio/skills"
30	  }
31	}
32	
```

> TOOL

tool_use Read
id: toolu_013Q56B125WNi7wL1LqxjGBn
```json
{
  "file_path": "/home/<USER>/Projects/skills/package.json"
}
```

> TOOL

tool_result
id: toolu_013Q56B125WNi7wL1LqxjGBn
```
1	{
2	  "name": "skills",
3	  "version": "0.1.0",
4	  "type": "module",
5	  "main": ".opencode/plugins/entire.js"
6	}
7	
```

> TOOL

tool_use Read
id: toolu_015sSLGLgxvoPeTaFzLyT2Qk
```json
{
  "file_path": "/home/<USER>/Projects/skills/.opencode/INSTALL.md"
}
```

> TOOL

tool_result
id: toolu_015sSLGLgxvoPeTaFzLyT2Qk
```
1	# Installing Skills for OpenCode
2	
3	Enable Entire skills in OpenCode via native skill discovery from `plugins/entire/skills`.
4	
5	## Prerequisites
6	
7	- [OpenCode.ai](https://opencode.ai) installed
8	
9	## Installation
10	
11	The published `skills` package installs the `entire` plugin from `plugins/entire`, which exposes the skills in `plugins/entire/skills`.
12	
13	Add to your OpenCode config:
14	
15	```json
16	{
17	  "plugin": ["skills@git+https://github.com/entireio/skills.git"]
18	}
19	```
20	
21	To pin a specific version:
22	
23	```json
24	{
25	  "plugin": ["skills@git+https://github.com/entireio/skills.git#v0.1.0"]
26	}
27	```
28	
29	Restart OpenCode. The plugin in `.opencode/plugins/entire.js` automatically registers the skills directory — no additional configuration needed.
30	
31	Verify by asking: "Use the `session-handoff` skill."
32	
```

> TOOL

tool_use Bash
id: toolu_01MNd4149AvTm3JeZduZroRy
```json
{
  "command": "ls /home/<USER>/Projects/skills/.agents/ /home/<USER>/Projects/skills/.claude/ /home/<USER>/Projects/skills/.codex/ /home/<USER>/Projects/skills/.opencode/",
  "description": "List agent-specific dirs"
}
```

> TOOL

tool_result
id: toolu_01MNd4149AvTm3JeZduZroRy
```
/home/<USER>/Projects/skills/.agents/:
plugins

/home/<USER>/Projects/skills/.claude/:
agents
settings.json
settings.local.json

/home/<USER>/Projects/skills/.codex/:
agents
config.toml
hooks.json

/home/<USER>/Projects/skills/.opencode/:
INSTALL.md
plugins
```

> TOOL

tool_use Read
id: toolu_01Wfiebfo8QwGcKx9qnpWTwk
```json
{
  "file_path": "/home/<USER>/Projects/skills/.agents/plugins/marketplace.json"
}
```

> TOOL

tool_result
id: toolu_01Wfiebfo8QwGcKx9qnpWTwk
```
1	{
2	  "name": "skills",
3	  "interface": {
4	    "displayName": "Skills"
5	  },
6	  "plugins": [
7	    {
8	      "name": "entire",
9	      "source": {
10	        "source": "local",
11	        "path": "./plugins/entire"
12	      },
13	      "policy": {
14	        "installation": "AVAILABLE",
15	        "authentication": "ON_INSTALL"
16	      },
17	      "category": "Development"
18	    }
19	  ]
20	}
21	
```

> TOOL

tool_use Bash
id: toolu_01NWGPjWvx22ksP4XvckMmUH
```json
{
  "command": "ls -la /home/<USER>/Projects/skills/.opencode/plugins/ /home/<USER>/Projects/skills/.codex/agents/ /home/<USER>/Projects/skills/.claude/agents/ 2>/dev/null",
  "description": "Check agent dirs"
}
```

> TOOL

tool_result
id: toolu_01NWGPjWvx22ksP4XvckMmUH
```
/home/<USER>/Projects/skills/.claude/agents/:
total 8
drwxr-x---@ 3 alisha  staff    96 Apr 10 12:53 .
drwxr-xr-x@ 5 alisha  staff   160 Apr 10 12:53 ..
-rw-------@ 1 alisha  staff  1517 Apr 10 12:53 entire-search.md

/home/<USER>/Projects/skills/.codex/agents/:
total 8
drwxr-x---@ 3 alisha  staff    96 Apr 10 12:53 .
drwxr-x---@ 5 alisha  staff   160 Apr 10 12:53 ..
-rw-------@ 1 alisha  staff  1563 Apr 10 12:53 entire-search.toml

/home/<USER>/Projects/skills/.opencode/plugins/:
total 8
drwxr-xr-x@ 3 alisha  staff   96 Apr 10 16:18 .
drwxr-xr-x@ 4 alisha  staff  128 Apr 10 16:18 ..
-rw-r--r--@ 1 alisha  staff  639 Apr 10 16:18 entire.js
```

> TOOL

tool_use Read
id: toolu_011fmQQ353pMYoDz2FsBbCiM
```json
{
  "file_path": "/home/<USER>/Projects/skills/.opencode/plugins/entire.js"
}
```

> TOOL

tool_result
id: toolu_011fmQQ353pMYoDz2FsBbCiM
```
1	/**
2	 * Entire plugin for OpenCode.ai
3	 *
4	 * Auto-registers the Entire skills directory via config hook.
5	 */
6	
7	import path from 'path';
8	import { fileURLToPath } from 'url';
9	
10	const __dirname = path.dirname(fileURLToPath(import.meta.url));
11	
12	export const EntirePlugin = async ({ client, directory }) => {
13	  const skillsDir = path.resolve(__dirname, '../../plugins/entire/skills');
14	
15	  return {
16	    config: async (config) => {
17	      config.skills = config.skills || {};
18	      config.skills.paths = config.skills.paths || [];
19	      if (!config.skills.paths.includes(skillsDir)) {
20	        config.skills.paths.push(skillsDir);
21	      }
22	    },
23	  };
24	};
25	
```

> TOOL

tool_use Bash
id: toolu_01LaqsxrUembkA7fh2fYvmko
```json
{
  "command": "ls /home/<USER>/Projects/skills/plugins/entire/skills/ /home/<USER>/Projects/skills/plugins/entire/skills/session-handoff/ 2>/dev/null",
  "description": "Check skills structure"
}
```

> TOOL

tool_result
id: toolu_01LaqsxrUembkA7fh2fYvmko
```
/home/<USER>/Projects/skills/plugins/entire/skills/:
explain
search
session-handoff

/home/<USER>/Projects/skills/plugins/entire/skills/session-handoff/:
SKILL.md
```

> TOOL

tool_use Bash
id: toolu_01KApnQfB8hwbybHiGLznHoF
```json
{
  "command": "ls /home/<USER>/Projects/skills/plugins/entire/ /home/<USER>/Projects/cc-skills-golang/skills/golang-code-style/ 2>/dev/null",
  "description": "Compare structures"
}
```

> TOOL

tool_result
id: toolu_01KApnQfB8hwbybHiGLznHoF
```
/home/<USER>/Projects/cc-skills-golang/skills/golang-code-style/:
SKILL.md
evals
references

/home/<USER>/Projects/skills/plugins/entire/:
skills
```

> AGENT

Now I understand the difference. `cc-skills-golang` uses a flat layout: skills live at `/skills/` at the repo root with `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, etc. at root. This repo nests everything under `plugins/entire/skills/`, which is why Cursor (and similar flat-discovery installs) break.

Let me plan and execute the refactor.

> TOOL

tool_use ToolSearch
id: toolu_01HjM1w9EfrLEAWH7jBqHBE3
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01HjM1w9EfrLEAWH7jBqHBE3
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
```

> TOOL

tool_use TaskCreate
id: toolu_01NHnpVpTYwvXk78ULj6cjD4
```json
{
  "subject": "Flatten skills dir to repo root",
  "description": "git mv plugins/entire/skills/* -> skills/* at repo root",
  "activeForm": "Flattening skills dir"
}
```

> TOOL

tool_result
id: toolu_01NHnpVpTYwvXk78ULj6cjD4
```
Task #1 created successfully: Flatten skills dir to repo root
```

> TOOL

tool_use TaskCreate
id: toolu_01TVKftncejwa7tYFgd7EkZq
```json
{
  "subject": "Move plugin manifests to repo root",
  "description": "Move .codex-plugin from plugins/entire to root, create .claude-plugin/plugin.json at root, remove marketplace nesting",
  "activeForm": "Moving plugin manifests"
}
```

> TOOL

tool_result
id: toolu_01TVKftncejwa7tYFgd7EkZq
```
Task #2 created successfully: Move plugin manifests to repo root
```

> TOOL

tool_use TaskCreate
id: toolu_01Xy8C3KFDngx3TXV88t6ync
```json
{
  "subject": "Update skills paths in manifests",
  "description": "Update .cursor-plugin, .opencode, .agents, and marketplace.json to point to ./skills/",
  "activeForm": "Updating skills paths"
}
```

> TOOL

tool_result
id: toolu_01Xy8C3KFDngx3TXV88t6ync
```
Task #3 created successfully: Update skills paths in manifests
```

> TOOL

tool_use TaskCreate
id: toolu_01LqKw8usG18k3RXYkVYKVQb
```json
{
  "subject": "Rewrite README install docs",
  "description": "Update README installation section to mirror cc-skills-golang per-agent install instructions",
  "activeForm": "Rewriting README install docs"
}
```

> TOOL

tool_result
id: toolu_01LqKw8usG18k3RXYkVYKVQb
```
Task #4 created successfully: Rewrite README install docs
```

> TOOL

tool_use TaskUpdate
id: toolu_013tN9t1iKrj61zZ4yTvcsgq
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_013tN9t1iKrj61zZ4yTvcsgq
```
Updated task #1 status
```

> TOOL

tool_use Bash
id: toolu_014DxDQyrbcVxZiSjfoWJRvF
```json
{
  "command": "git mv plugins/entire/skills skills && ls skills/",
  "description": "Move skills dir to root"
}
```

> TOOL

tool_result
id: toolu_014DxDQyrbcVxZiSjfoWJRvF
```
explain
search
session-handoff
```

> TOOL

tool_use TaskUpdate
id: toolu_0155puAmVc8nKoxdWJ6bnAPT
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_0155puAmVc8nKoxdWJ6bnAPT
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01PPkZEFx3TtZhbdAdyaUkXW
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01PPkZEFx3TtZhbdAdyaUkXW
```
Updated task #2 status
```

> AGENT

Now move the codex plugin manifest to the root, replace the claude marketplace with a plugin manifest, and delete the now-empty nested plugin dir.

> TOOL

tool_use Bash
id: toolu_01HwGuhs3SKBK292mYJUAnnW
```json
{
  "command": "mkdir -p .codex-plugin && git mv plugins/entire/.codex-plugin/plugin.json .codex-plugin/plugin.json && ls .codex-plugin/",
  "description": "Move codex plugin to root"
}
```

> TOOL

tool_result
id: toolu_01HwGuhs3SKBK292mYJUAnnW
```
plugin.json
```

> TOOL

tool_use Bash
id: toolu_01YZbb1BSSGUAjSLgYbgTCFZ
```json
{
  "command": "git mv plugins/entire/.claude-plugin/plugin.json .claude-plugin/plugin.json 2>&1",
  "description": "Move claude plugin.json to root .claude-plugin dir"
}
```

> TOOL

tool_result
id: toolu_01YZbb1BSSGUAjSLgYbgTCFZ
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01YKYC3hk1kYDmgAtKpyxSGe
```json
{
  "command": "ls -la .claude-plugin/ plugins/entire/ 2>&1",
  "description": "Verify state"
}
```

> TOOL

tool_result
id: toolu_01YKYC3hk1kYDmgAtKpyxSGe
```
.claude-plugin/:
total 16
drwxr-xr-x@  4 alisha  staff  128 Apr 24 09:52 .
drwxr-xr-x@ 19 alisha  staff  608 Apr 24 09:52 ..
-rw-r--r--@  1 alisha  staff  525 Apr 10 13:31 marketplace.json
-rw-r--r--@  1 alisha  staff  386 Apr 10 13:31 plugin.json

plugins/entire/:
total 0
drwxr-xr-x@ 4 alisha  staff  128 Apr 24 09:52 .
drwxr-xr-x@ 3 alisha  staff   96 Apr 10 11:28 ..
drwxr-xr-x@ 2 alisha  staff   64 Apr 24 09:52 .claude-plugin
drwxr-xr-x@ 2 alisha  staff   64 Apr 24 09:52 .codex-plugin
```

> AGENT

Now remove empty nested dirs.

> TOOL

tool_use Bash
id: toolu_0131iyr3QNrRG8G49VTfUjhy
```json
{
  "command": "rmdir plugins/entire/.claude-plugin plugins/entire/.codex-plugin plugins/entire plugins 2>&1; ls",
  "description": "Remove empty nested plugin dirs"
}
```

> TOOL

tool_result
id: toolu_0131iyr3QNrRG8G49VTfUjhy
```
GEMINI.md
README.md
docs
gemini-extension.json
package.json
skills
```

> TOOL

tool_use TaskUpdate
id: toolu_01MWAeg9TiBidqvLBZfa1WYY
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01MWAeg9TiBidqvLBZfa1WYY
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01CRTpxS6XhqnspRrdTThzUf
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01CRTpxS6XhqnspRrdTThzUf
```
Updated task #3 status
```

> AGENT

Now update all skill path references. Start with the cursor manifest, marketplace, opencode plugin, agents marketplace, and package.json.

> TOOL

tool_use Edit
id: toolu_01TeJr4GhfKU1XPcFiWyP9jB
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.cursor-plugin/plugin.json",
  "old_string": "  \"skills\": \"./plugins/entire/skills/\"",
  "new_string": "  \"skills\": \"./skills/\""
}
```

> TOOL

tool_result
id: toolu_01TeJr4GhfKU1XPcFiWyP9jB
```
The file /home/<USER>/Projects/skills/.cursor-plugin/plugin.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_012MrxFAfqmLRTfqD97Kw9sy
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.codex-plugin/plugin.json",
  "old_string": "  \"skills\": \"./skills/\",",
  "new_string": "  \"skills\": \"./skills/\",\n  \"_comment\": \"skills path is relative to repo root\","
}
```

> TOOL

tool_result ERROR
id: toolu_012MrxFAfqmLRTfqD97Kw9sy
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> AGENT

Actually the codex manifest already says `"skills": "./skills/"` which is correct since it's now at root. No change needed.

> TOOL

tool_use Read
id: toolu_01UArhoZpXJwErjpGrnN2R9Q
```json
{
  "file_path": "/home/<USER>/Projects/skills/.codex-plugin/plugin.json"
}
```

> TOOL

tool_result
id: toolu_01UArhoZpXJwErjpGrnN2R9Q
```
1	{
2	  "name": "entire",
3	  "version": "0.1.0",
4	  "description": "Cross-agent skills and commands powered by Entire.",
5	  "author": {
6	    "name": "Entire Inc",
7	    "url": "https://github.com/entireio"
8	  },
9	  "homepage": "https://github.com/entireio/skills",
10	  "repository": "https://github.com/entireio/skills",
11	  "license": "MIT",
12	  "keywords": [
13	    "entire",
14	    "session-handoff",
15	    "handoff",
16	    "agent-workflows",
17	    "skills"
18	  ],
19	  "skills": "./skills/",
20	  "interface": {
21	    "displayName": "Entire",
22	    "shortDescription": "Continue work across agents with session handoff",
23	    "developerName": "Entire Inc",
24	    "category": "Development",
25	    "capabilities": [
26	      "Interactive",
27	      "Write"
28	    ],
29	    "websiteURL": "https://github.com/entireio/skills"
30	  }
31	}
32	
```

> AGENT

Good — codex manifest is correct. Now update the marketplace.json to treat the root as the plugin source.

> TOOL

tool_use Edit
id: toolu_01BDuRcCoYwvTqSQ26x6ypwP
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.claude-plugin/marketplace.json",
  "old_string": "      \"source\": \"./plugins/entire\",",
  "new_string": "      \"source\": \"./\","
}
```

> TOOL

tool_result
id: toolu_01BDuRcCoYwvTqSQ26x6ypwP
```
The file /home/<USER>/Projects/skills/.claude-plugin/marketplace.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01VSpj9Jd9s7cna9ZdCHsvQG
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.agents/plugins/marketplace.json",
  "old_string": "      \"source\": {\n        \"source\": \"local\",\n        \"path\": \"./plugins/entire\"\n      },",
  "new_string": "      \"source\": {\n        \"source\": \"local\",\n        \"path\": \"./\"\n      },"
}
```

> TOOL

tool_result
id: toolu_01VSpj9Jd9s7cna9ZdCHsvQG
```
The file /home/<USER>/Projects/skills/.agents/plugins/marketplace.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_019wDyBQEAk6keafFfd2WjWa
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.opencode/plugins/entire.js",
  "old_string": "  const skillsDir = path.resolve(__dirname, '../../plugins/entire/skills');",
  "new_string": "  const skillsDir = path.resolve(__dirname, '../../skills');"
}
```

> TOOL

tool_result
id: toolu_019wDyBQEAk6keafFfd2WjWa
```
The file /home/<USER>/Projects/skills/.opencode/plugins/entire.js has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me check if there are any other references to the old `plugins/entire/skills` path.

> TOOL

tool_use Bash
id: toolu_01EHuFEx8tD4gXV1pvf2wnDM
```json
{
  "command": "grep -rln \"plugins/entire\" /home/<USER>/Projects/skills --exclude-dir=.git --exclude-dir=.entire 2>&1",
  "description": "Find remaining refs to old path"
}
```

> TOOL

tool_result
id: toolu_01EHuFEx8tD4gXV1pvf2wnDM
```
/home/<USER>/Projects/skills/README.md
/home/<USER>/Projects/skills/package.json
/home/<USER>/Projects/skills/GEMINI.md
/home/<USER>/Projects/skills/.opencode/INSTALL.md
```

> TOOL

tool_use Read
id: toolu_019VqZCATf2tkr6rjP55HBpP
```json
{
  "file_path": "/home/<USER>/Projects/skills/GEMINI.md"
}
```

> TOOL

tool_result
id: toolu_019VqZCATf2tkr6rjP55HBpP
```
1	@./plugins/entire/skills/session-handoff/SKILL.md
2	
```

> TOOL

tool_use Edit
id: toolu_01F4NaX9AhayaxcnWZXKECkd
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/GEMINI.md",
  "old_string": "@./plugins/entire/skills/session-handoff/SKILL.md",
  "new_string": "@./skills/session-handoff/SKILL.md"
}
```

> TOOL

tool_result
id: toolu_01F4NaX9AhayaxcnWZXKECkd
```
The file /home/<USER>/Projects/skills/GEMINI.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
id: toolu_01XBKhMnFdKUEpdpP3hfF65p
```json
{
  "file_path": "/home/<USER>/Projects/skills/package.json"
}
```

> TOOL

tool_result
id: toolu_01XBKhMnFdKUEpdpP3hfF65p
```
1	{
2	  "name": "skills",
3	  "version": "0.1.0",
4	  "type": "module",
5	  "main": ".opencode/plugins/entire.js"
6	}
7	
```

> TOOL

tool_use Bash
id: toolu_01FY6RyVvJXKAGedCE5HYZeK
```json
{
  "command": "grep -n \"plugins/entire\" /home/<USER>/Projects/skills/package.json /home/<USER>/Projects/skills/.opencode/INSTALL.md 2>&1",
  "description": "Check context"
}
```

> TOOL

tool_result
id: toolu_01FY6RyVvJXKAGedCE5HYZeK
```
/home/<USER>/Projects/skills/package.json:5:  "main": ".opencode/plugins/entire.js"
/home/<USER>/Projects/skills/.opencode/INSTALL.md:3:Enable Entire skills in OpenCode via native skill discovery from `plugins/entire/skills`.
/home/<USER>/Projects/skills/.opencode/INSTALL.md:11:The published `skills` package installs the `entire` plugin from `plugins/entire`, which exposes the skills in `plugins/entire/skills`.
/home/<USER>/Projects/skills/.opencode/INSTALL.md:29:Restart OpenCode. The plugin in `.opencode/plugins/entire.js` automatically registers the skills directory — no additional configuration needed.
```

> AGENT

package.json main is fine (that's `.opencode/plugins/entire.js`, a real file path). Fix INSTALL.md.

> TOOL

tool_use Edit
id: toolu_01PgBX5zD5zGmsci43Mic1Dv
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.opencode/INSTALL.md",
  "old_string": "Enable Entire skills in OpenCode via native skill discovery from `plugins/entire/skills`.",
  "new_string": "Enable Entire skills in OpenCode via native skill discovery from `skills/`."
}
```

> TOOL

tool_result
id: toolu_01PgBX5zD5zGmsci43Mic1Dv
```
The file /home/<USER>/Projects/skills/.opencode/INSTALL.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01VC6J9N6E9Hvxad7Yctio8X
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/.opencode/INSTALL.md",
  "old_string": "The published `skills` package installs the `entire` plugin from `plugins/entire`, which exposes the skills in `plugins/entire/skills`.",
  "new_string": "The published `skills` package installs the `entire` plugin, which exposes the skills in `./skills/`."
}
```

> TOOL

tool_result
id: toolu_01VC6J9N6E9Hvxad7Yctio8X
```
The file /home/<USER>/Projects/skills/.opencode/INSTALL.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
id: toolu_01Bqp2Gxg3soyatZw6n2iYtB
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01Bqp2Gxg3soyatZw6n2iYtB
```
Updated task #3 status
```

> TOOL

tool_use TaskUpdate
id: toolu_015wKvSo7rRVFnSJx7rP239K
```json
{
  "taskId": "4",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_015wKvSo7rRVFnSJx7rP239K
```
Updated task #4 status
```

> AGENT

Now rewrite the README install section. I'll keep the existing skill descriptions but replace the install section to mirror cc-skills-golang's per-agent collapsibles.

> TOOL

tool_use Edit
id: toolu_013QBwkeXyMoCY9hhuPiWGF5
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Projects/skills/README.md",
  "old_string": "## Installation\n\nInstall the agent that matches your workflow from its marketplace, manifest, or install-doc entrypoint:\n\n### Claude Code (via Plugin Marketplace)\n\nIn Claude Code, register the marketplace first:\n\n```bash\n/plugin marketplace add entireio/skills\n```\n\nThen install the plugin from this marketplace:\n\n```bash\n/plugin install entire \n```\n\n### Codex\n\nUse `plugins/entire/.codex-plugin/plugin.json`.\n\n### OpenCode\n\nUse the package-based flow in `.opencode/INSTALL.md`.\n\n### Cursor\n\nUse `.cursor-plugin/plugin.json`.\n\n### Gemini\n\n```bash\ngemini extensions install https://github.com/entireio/skills\n```",
  "new_string": "## Installation\n\nInstall with [skills](https://skills.sh/) CLI (universal, works with any [Agent Skills](https://agentskills.io)-compatible tool):\n\n```bash\nnpx skills add https://github.com/entireio/skills --all\n# or a single skill:\nnpx skills add https://github.com/entireio/skills --skill session-handoff\n```\n\n<!-- prettier-ignore-start -->\n\n<details>\n<summary>Claude Code</summary>\n\n```bash\n/plugin marketplace add entireio/skills\n/plugin install entire\n```\n\n</details>\n\n<details>\n<summary>Cursor</summary>\n\nCopy skills into the cross-client discovery directory:\n\n```bash\ngit clone https://github.com/entireio/skills.git ~/.cursor/skills/entire\n```\n\nCursor auto-discovers skills from `.agents/skills/` and `.cursor/skills/`.\n\n</details>\n\n<details>\n<summary>Gemini CLI</summary>\n\n```bash\ngemini extensions install https://github.com/entireio/skills\n```\n\nUpdate with `gemini extensions update entire`.\n\n</details>\n\n<details>\n<summary>OpenCode</summary>\n\nAdd to your OpenCode config:\n\n```json\n{\n  \"plugin\": [\"skills@git+https://github.com/entireio/skills.git\"]\n}\n```\n\nOpenCode auto-registers the skills directory via `.opencode/plugins/entire.js`. See [`.opencode/INSTALL.md`](.opencode/INSTALL.md) for details.\n\n</details>\n\n<details>\n<summary>Codex (OpenAI)</summary>\n\nClone into the cross-client discovery path:\n\n```bash\ngit clone https://github.com/entireio/skills.git ~/.agents/skills/entire\n```\n\nCodex auto-discovers skills from `~/.agents/skills/` and `.agents/skills/`. Update with `cd ~/.agents/skills/entire && git pull`.\n\n</details>\n\n<details>\n<summary>Copilot</summary>\n\n```bash\n/plugin install https://github.com/entireio/skills\n# or\ngit clone https://github.com/entireio/skills.git ~/.copilot/skills/entire\n```\n\nCopilot auto-discovers skills from `.copilot/skills/`.\n\n</details>\n\n<!-- prettier-ignore-end -->"
}
```

> TOOL

tool_result
id: toolu_013QBwkeXyMoCY9hhuPiWGF5
```
The file /home/<USER>/Projects/skills/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
id: toolu_01ToMrWxtqL1SQ8PGyHAaihi
```json
{
  "taskId": "4",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01ToMrWxtqL1SQ8PGyHAaihi
```
Updated task #4 status
```

> AGENT

Let me verify the final state.

> TOOL

tool_use Bash
id: toolu_01RqfH4HPmh6bhgiDV95Whbu
```json
{
  "command": "ls -la && echo \"---skills/---\" && ls skills/ && echo \"---.claude-plugin/---\" && ls .claude-plugin/ && echo \"---.cursor-plugin/---\" && ls .cursor-plugin/ && echo \"---.codex-plugin/---\" && ls .codex-plugin/",
  "description": "Verify final layout"
}
```

> TOOL

tool_result
id: toolu_01RqfH4HPmh6bhgiDV95Whbu
```
total 48
drwxr-xr-x@ 18 alisha  staff   576 Apr 24 09:53 .
drwxr-xr-x@ 36 alisha  staff  1152 Apr 24 09:46 ..
drwxr-xr-x@  3 alisha  staff    96 Apr 10 10:35 .agents
drwxr-xr-x@  5 alisha  staff   160 Apr 10 12:53 .claude
drwxr-xr-x@  4 alisha  staff   128 Apr 24 09:53 .claude-plugin
drwxr-x---@  5 alisha  staff   160 Apr 10 12:53 .codex
drwxr-xr-x@  3 alisha  staff    96 Apr 24 09:52 .codex-plugin
drwxr-xr-x@  3 alisha  staff    96 Apr 24 09:53 .cursor-plugin
drwxr-x---@  7 alisha  staff   224 Apr 10 13:21 .entire
drwxr-xr-x@ 17 alisha  staff   544 Apr 24 09:52 .git
-rw-r--r--@  1 alisha  staff     4 Apr 10 13:20 .gitignore
drwxr-xr-x@  4 alisha  staff   128 Apr 24 09:53 .opencode
-rw-r--r--@  1 alisha  staff    35 Apr 24 09:53 GEMINI.md
-rw-r--r--@  1 alisha  staff  4576 Apr 24 09:53 README.md
drwxr-xr-x@  3 alisha  staff    96 Apr 17 11:14 docs
-rw-r--r--@  1 alisha  staff   150 Apr 10 12:21 gemini-extension.json
-rw-r--r--@  1 alisha  staff   106 Apr 10 16:37 package.json
drwxr-xr-x@  5 alisha  staff   160 Apr 24 09:48 skills
---skills/---
explain
search
session-handoff
---.claude-plugin/---
marketplace.json
plugin.json
---.cursor-plugin/---
plugin.json
---.codex-plugin/---
plugin.json
```

> TOOL

tool_use Bash
id: toolu_01QrEFXAZiHvZNRgkEpqzxpQ
```json
{
  "command": "grep -rln \"plugins/entire\" /home/<USER>/Projects/skills --exclude-dir=.git --exclude-dir=.entire --exclude-dir=docs 2>&1",
  "description": "Final check for stale path references"
}
```

> TOOL

tool_result
id: toolu_01QrEFXAZiHvZNRgkEpqzxpQ
```
/home/<USER>/Projects/skills/README.md
/home/<USER>/Projects/skills/package.json
/home/<USER>/Projects/skills/.opencode/INSTALL.md
```

> TOOL

tool_use Bash
id: toolu_01AxzURxcNMzGqj7Hhtdn4kj
```json
{
  "command": "grep -n \"plugins/entire\" README.md package.json .opencode/INSTALL.md 2>&1",
  "description": "See remaining refs in context"
}
```

> TOOL

tool_result
id: toolu_01AxzURxcNMzGqj7Hhtdn4kj
```
package.json:5:  "main": ".opencode/plugins/entire.js"
README.md:109:OpenCode auto-registers the skills directory via `.opencode/plugins/entire.js`. See [`.opencode/INSTALL.md`](.opencode/INSTALL.md) for details.
.opencode/INSTALL.md:29:Restart OpenCode. The plugin in `.opencode/plugins/entire.js` automatically registers the skills directory — no additional configuration needed.
```

> AGENT

All three are valid references to the real file `.opencode/plugins/entire.js` — those stay. Final check of git state:

> TOOL

tool_use Bash
id: toolu_01EBBcyc3kFtPaQ7wmnJDM3W
```json
{
  "command": "git status",
  "description": "Show git state"
}
```

> TOOL

tool_result
id: toolu_01EBBcyc3kFtPaQ7wmnJDM3W
```
On branch alisha/refactor
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	renamed:    plugins/entire/.claude-plugin/plugin.json -> .claude-plugin/plugin.json
	renamed:    plugins/entire/.codex-plugin/plugin.json -> .codex-plugin/plugin.json
	renamed:    plugins/entire/skills/explain/SKILL.md -> skills/explain/SKILL.md
	renamed:    plugins/entire/skills/search/SKILL.md -> skills/search/SKILL.md
	renamed:    plugins/entire/skills/session-handoff/SKILL.md -> skills/session-handoff/SKILL.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .agents/plugins/marketplace.json
	modified:   .claude-plugin/marketplace.json
	modified:   .cursor-plugin/plugin.json
	modified:   .opencode/INSTALL.md
	modified:   .opencode/plugins/entire.js
	modified:   GEMINI.md
	modified:   README.md
```

> AGENT

Layout now matches `cc-skills-golang`:

- `skills/{explain,search,session-handoff}/SKILL.md` at repo root (git-tracked rename, history preserved)
- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (source now `./`)
- `.cursor-plugin/plugin.json` with `"skills": "./skills/"`
- `.codex-plugin/plugin.json` at root with `"skills": "./skills/"`
- `.opencode/plugins/entire.js` resolves to `../../skills`
- `.agents/plugins/marketplace.json` source `./`
- `GEMINI.md` imports from `./skills/session-handoff/SKILL.md`
- `plugins/` directory removed
- `README.md` install section rewritten with per-agent collapsible sections (Claude Code, Cursor, Gemini, OpenCode, Codex, Copilot)

The `git clone ... ~/.cursor/skills/entire` flow for Cursor will now work because skills live at the conventional top-level `skills/` path. Want me to commit and push, or test a specific agent install first?