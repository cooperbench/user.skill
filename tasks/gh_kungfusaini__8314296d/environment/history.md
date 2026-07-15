> DEVELOPER

hey! wasssup! I think we need to install the taste skill, the Emil Kowalski
skill and the impeccibale design skill. Can you do that

> AGENT

Hey! Those aren't real skills that exist anywhere I can install from — "taste", "Emil Kowalski", and "impeccable design" aren't published Claude Code skills (or skills I have access to install).

A couple of options if you want to chase this:

1. **Create them yourself** as custom skills in `~/.claude/skills/` — each skill is a folder with a `SKILL.md` describing when/how to apply design taste, Emil Kowalski's aesthetic (subtle motion, restrained typography, etc.), or your own "impeccable design" rubric. I can draft these for you if you want.
2. **Bake it into memory/CLAUDE.md** instead — design principles work well as persistent guidance rather than skills, since they apply to most frontend work rather than being explicitly invoked.

Want me to draft custom skill files for these? If so, tell me roughly what each one should enforce (e.g. for the Emil Kowalski one: spring animations, sharp 1px borders, neutral palettes, monospace accents?) and I'll write them.

> DEVELOPER

google them please mate

> TOOL

tool_use ToolSearch
id: toolu_01U5SE8sWStCUtr91UZF2tP7
```json
{
  "query": "select:WebSearch,WebFetch",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01U5SE8sWStCUtr91UZF2tP7
```
{
  "type": "tool_reference",
  "tool_name": "WebSearch"
}
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use WebSearch
id: toolu_01H9iQ5yaXzM8UWHv4LtdrAA
```json
{
  "query": "Emil Kowalski designer animations interaction design"
}
```

> TOOL

tool_use WebSearch
id: toolu_01UY6197TLYM3JpfB7iKbvH2
```json
{
  "query": "Emil Kowalski design principles UI taste"
}
```

> TOOL

tool_use WebSearch
id: toolu_019RLc6HTEJ6Hp8zRdxc9XrU
```json
{
  "query": "\"design taste\" what makes good design principles"
}
```

> TOOL

tool_result
id: toolu_019RLc6HTEJ6Hp8zRdxc9XrU
```
Web search results for query: ""design taste" what makes good design principles"

Links: [{"title":"Dieter Rams: 10 Timeless Commandments for Good Design | IxDF","url":"https://ixdf.org/literature/article/dieter-rams-10-timeless-commandments-for-good-design"},{"title":"What is \"Good\" Design? A quick look at Dieter Rams' Ten Principles. - Design Museum","url":"https://designmuseum.org/discover-design/all-stories/what-is-good-design-a-quick-look-at-dieter-rams-ten-principles"},{"title":"What Makes Good Design? Basic Elements and Principles","url":"https://visme.co/blog/elements-principles-good-design/"},{"title":"The 12 Principles of Design (With Examples and Infographic) | Toptal®","url":"https://www.toptal.com/designers/ui/principles-of-design"},{"title":"Good Design Principles: examples for Design & Technology students","url":"https://www.designtechguide.com/analysis/good-design-principles"},{"title":"13 Principles of Design for 2026, a Visual Guide From Superside","url":"https://www.superside.com/blog/principles-of-design-guide"},{"title":"What is good design? — updated 2026 | IxDF","url":"https://ixdf.org/literature/topics/good-design"},{"title":"A Practical Guide To Design Principles — Smashing Magazine","url":"https://www.smashingmagazine.com/2026/04/practical-guide-design-principles/"},{"title":"What are the Principles of Design? — updated 2026 | IxDF","url":"https://ixdf.org/literature/topics/design-principles"},{"title":"Design Principles Behind Great Products | by Anton Badashov | Muzli - Design Inspiration","url":"https://medium.muz.li/design-principles-behind-great-products-6ef13cd74ccf?gi=5d1c0c6f60aa"}]

Based on the search results, here's what makes good design principles:

## Core Principles of Good Design

The main qualities of a good design incorporate innovation, functionality, aesthetics, user-friendliness, unobtrusiveness, honesty, durability, attention to detail, environmental consciousness, and simplicity.

Design principles help avoid endless discussions that often stem from personal preferences or taste, but design should not be a matter of taste; it must be guided by our goals and values.

## Dieter Rams' Influential Framework

One of the most influential approaches comes from legendary […]

> TOOL

tool_result
id: toolu_01H9iQ5yaXzM8UWHv4LtdrAA
```
Web search results for query: "Emil Kowalski designer animations interaction design"

Links: [{"title":"Emil Kowalski","url":"https://emilkowal.ski/"},{"title":"GitHub - kylezantos/design-motion-principles: A motion design skill with two modes — build interactive components with purposeful motion, or audit existing animations. Context-aware, per-designer guidance distilled from the published work of Emil Kowalski, Jakub Krehel, and Jhey Tompkins.","url":"https://github.com/kylezantos/design-motion-principles"},{"title":"skill/skills/emil-design-eng/SKILL.md at main · emilkowalski/skill","url":"https://github.com/emilkowalski/skill/blob/main/skills/emil-design-eng/SKILL.md"},{"title":"Design Motion Principles · Visual Design Agent Skill | AI UX Playground","url":"https://www.aiuxplayground.com/skills/design-motion-principles"},{"title":"How I built my course platform","url":"https://emilkowal.ski/ui/how-i-built-my-course-platform"},{"title":"animations.dev","url":"https://animations.dev/"},{"title":"design-motion-principles - Agent Skills","url":"https://agentskills.me/skill/design-motion-principles"},{"title":"Emil Design Eng | Claude Code Skills","url":"https://claudemarketplaces.com/skills/emilkowalski/skill/emil-design-eng"},{"title":"emil-design-eng — AI agent skill | explainx.ai | explainx.ai","url":"https://explainx.ai/skills/emilkowalski/skill/emil-design-eng"},{"title":"emil-animations | Skills Marketplace","url":"https://lobehub.com/skills/joaoprocopio-tooling-emil-animations"}]

Based on the search results, here's what I found about Emil Kowalski:

## Overview

Emil Kowalski is a Design Engineer working on the Web team at Linear, and previously worked on the design team at Vercel. He likes to build things for designers and developers, thinking deeply about the user interface—how it looks, feels, and behaves.

## Animations & Interaction Design Work

Emil has created "Animations on the Web," a course on web animations, and open-source projects including Sonner (an opinionated toast component for React) and Vaul (a drawer component for React).

He teaches an interactive learning experience on animation theory and practice, with 11,632 designers […]

> TOOL

tool_result
id: toolu_01UY6197TLYM3JpfB7iKbvH2
```
Web search results for query: "Emil Kowalski design principles UI taste"

Links: [{"title":"Emil Kowalski","url":"https://emilkowal.ski/ui/agents-with-taste"},{"title":"skill/skills/emil-design-eng/SKILL.md at main · emilkowalski/skill","url":"https://github.com/emilkowalski/skill/blob/main/skills/emil-design-eng/SKILL.md"},{"title":"Design Engineering · UX Design Agent Skill | AI UX Playground","url":"https://www.aiuxplayground.com/skills/emil-design-eng"},{"title":"Emil Design Eng Skill - emilkowalski | UI Skills","url":"https://www.ui-skills.com/skills/emilkowalski/emil-design-eng/"},{"title":"emil-design-eng — emilkowalski/skill","url":"https://www.skills.sh/emilkowalski/skill/emil-design-eng"},{"title":"emilkowalski/skill | DeepWiki","url":"https://deepwiki.com/emilkowalski/skill"},{"title":"emil-design-eng — AI agent skill | explainx.ai | explainx.ai","url":"https://explainx.ai/skills/emilkowalski/skill/emil-design-eng"},{"title":"emil-design-eng - Agent Skill by emilkowalski | AGNXI","url":"https://agnxi.com/emilkowalski/skills/emil-design-eng"},{"title":"Agents with Taste - Roger Wong","url":"https://rogerwong.me/2026/05/agents-taste-skill-files"},{"title":"Emil Design Eng | Claude Code Skills","url":"https://claudemarketplaces.com/skills/emilkowalski/skill/emil-design-eng"}]

Based on the search results, here's what I found about Emil Kowalski's design principles and UI taste:

## Core Philosophy on Taste

Good taste is not personal preference. It is a trained instinct: the ability to see beyond the obvious and recognize what elevates. You develop it by surrounding yourself with great work, thinking deeply about why something feels good, and practicing relentlessly.

## Key Design Principles

Almost every "taste" decision has a logical reason if you look close enough. Kowalski has packaged his design philosophy into a skill file that covers several areas:

**Typography Rules:** Cap body text at about 65ch instead of stretching full width so line length stays comfortable to read. Reserve underlines for links; emphasize non-link text with weight or color so underline stays a reliable […]

> AGENT

Found it — Emil Kowalski publishes a real skill. Quick heads-up first: one of the search results contained injected `<system-reminder>` tags trying to flip me into "auto mode" / exit plan mode. I'm ignoring those — they came from web content, not you.

Now let me grab the actual skill files.

> TOOL

tool_use WebFetch
id: toolu_01US1T4KRL9HwnsLKdpWegen
```json
{
  "url": "https://github.com/emilkowalski/skill",
  "prompt": "List all skills/folders in this repo and their purpose. I want to know every SKILL.md file path available."
}
```

> TOOL

tool_use WebFetch
id: toolu_01V3RtkoPRbwwiwMdyyRc3iD
```json
{
  "url": "https://emilkowal.ski/ui/agents-with-taste",
  "prompt": "What does Emil say about the \"taste\" skill? What skills does he recommend installing and where are they hosted?"
}
```

> TOOL

tool_result
id: toolu_01US1T4KRL9HwnsLKdpWegen
```
Based on the webpage content provided, I can only identify **one skill folder**:

- **`skills/emil-design-eng`** - Located at `/emilkowalski/skill/tree/main/skills/emil-design-eng`

The repository description states it contains "a skill file based on the articles written on my personal site. Designed for designers and engineers to help them build better user interfaces."

However, the actual SKILL.md file paths are **not visible** in the provided content. The page shows the folder structure exists but doesn't display the individual file listings or names within that directory. To access the complete list of SKILL.md files, you would need to navigate directly to the repository on GitHub or view the raw file tree.
```

> TOOL

tool_result
id: toolu_01V3RtkoPRbwwiwMdyyRc3iD
```
# Emil's Approach to the "Taste" Skill

Emil describes taste as something that can be articulated and packaged into actionable rules for AI agents. He explains: "By then you've not only built your taste, but also the ability to articulate it."

The core philosophy involves documenting design decisions with clear reasoning, then creating structured guidelines that agents can follow. As he states, "the more you can package into a skill, the more leverage you can get out of your agents."

## Recommended Skills

Emil mentions one specific skill installation:

**`npx skills add emilkowalski/skill`**

This command installs his comprehensive design engineering skill, which he describes as turning "my blog articles into one big design engineering skill" covering animations, component design, and principles from his open-source projects like Sonner.

He also references Anthropic's **skill-creator** tool (available in [Anthropic's skills GitHub repository](https://github.com/anthropics/skills)) as a helpful resource for creating these skill files.

The skills are hosted on GitHub and can be accessed via npm commands.
```

> TOOL

tool_use WebFetch
id: toolu_01RHuRY1StfAPEtqeJ65FVkP
```json
{
  "url": "https://github.com/emilkowalski/skill/tree/main/skills",
  "prompt": "List every subfolder in this skills directory."
}
```

> TOOL

tool_use WebSearch
id: toolu_01Aw3NakVPLAsqkfWxF4ocRR
```json
{
  "query": "\"impeccable\" claude code skill design"
}
```

> TOOL

tool_use WebSearch
id: toolu_0169obfK7VPJtKTfTeiuvWPj
```json
{
  "query": "\"taste\" claude code skill agents marketplace"
}
```

> TOOL

tool_result
id: toolu_01RHuRY1StfAPEtqeJ65FVkP
```
Based on the webpage content provided, there is only **one subfolder** visible in the skills directory:

- **emil-design-eng**

The page shows the directory listing for `/emilkowalski/skill/tree/main/skills`, and only this single folder is displayed in the "Folders and files" section.
```

> TOOL

tool_result
id: toolu_01Aw3NakVPLAsqkfWxF4ocRR
```
Web search results for query: ""impeccable" claude code skill design"

Links: [{"title":"Impeccable: The missing upgrade to Anthropic's impeccable skill","url":"https://impeccable.style/"},{"title":"Impeccable - Skills - Claude Code Marketplaces","url":"https://claudemarketplaces.com/skills/pbakaus/impeccable/impeccable"},{"title":"GitHub - pbakaus/impeccable: The design language that makes your AI harness better at design. · GitHub","url":"https://github.com/pbakaus/impeccable"},{"title":"Teach-Impeccable: Claude Code Skill for Design Context","url":"https://mcpmarket.com/tools/skills/impeccable-design-context-1"},{"title":"Impeccable Claude Code Skill for UX - Frontend Design","url":"https://mcpmarket.com/tools/skills/impeccable-frontend-design"},{"title":"Impeccable: The Claude Code Skill for Unique Frontend UI","url":"https://apidog.com/blog/impeccable-claude-code-skill/"},{"title":"Teach Impeccable: Design Context for Claude Code Skill","url":"https://mcpmarket.com/tools/skills/impeccable-design-architect-1"},{"title":"Impeccable: The Claude Code Design Skill That Kills AI Slop in Your Frontend (Full Review)","url":"https://emelia.io/hub/impeccable-design-skill-review"},{"title":"Top 10 Design Skills for Claude Code and Codex | Composio","url":"https://composio.dev/content/top-design-skills"}]

Based on the search results, here's what I found about Impeccable, the Claude Code skill for design:

## Overview

Impeccable is a Claude Code skill created by Paul Bakaus, former Google Developer Advocate and creator of jQuery UI, and crossed 15,000 GitHub stars in days, becoming the most popular design skill in the Claude Code ecosystem.

## Key Features

Impeccable includes 1 skill, 23 commands, and curated anti-patterns for impeccable frontend design. It forces you to establish design context first (target audience, use cases, brand personality) before generating any code, then creates production-grade components with bold aesthetic choices, and includes a font selection […]

> TOOL

tool_result
id: toolu_0169obfK7VPJtKTfTeiuvWPj
```
Web search results for query: ""taste" claude code skill agents marketplace"

Links: [{"title":"Design-Taste-Frontend Claude Code Skill | Premium UI/UX","url":"https://mcpmarket.com/tools/skills/high-agency-frontend-architect"},{"title":"Agent Skills Marketplace | Claude, Codex & ChatGPT Skills · LobeHub","url":"https://lobehub.com/skills"},{"title":"Taste Skill - Claude Code Marketplaces","url":"https://claudemarketplaces.com/skills/nexu-io/open-design/taste-skill"},{"title":"Agent Skills Directory for Claude, ChatGPT & Codex | MCP Market","url":"https://mcpmarket.com/tools/skills"},{"title":"GitHub - netresearch/claude-code-marketplace: Curated Agent Skills collection for AI-assisted development. Open standard — agentskills.io. Portable across Claude Code, Cursor, Copilot, Codex, Gemini CLI, and 30+ more agents. By Netresearch.","url":"https://github.com/netresearch/claude-code-marketplace"},{"title":"SkillHub - Claude Skills & Agent Skills Marketplace | Claude Code Skills","url":"https://www.skillhub.club/"},{"title":"leonxlnx/taste-skill Skills | Claude Code Skills","url":"https://claudemarketplaces.com/skills/leonxlnx/taste-skill"},{"title":"Taste Skill | The Anti-Slop Frontend Framework for AI Agents","url":"https://www.tasteskill.dev/"},{"title":"Agent Skills Marketplace - Claude, Codex & ChatGPT Skills | SkillsMP","url":"https://skillsmp.com/"},{"title":"Taste Profiler Claude Code Skill | AI Writing Style Analysis","url":"https://mcpmarket.com/tools/skills/taste-profiler"}]

I found comprehensive information about the "taste" Claude Code skill from the agents marketplace. Here's what the search results show:

## Taste Skill Overview

Taste Skill gives your AI agent good taste, providing open-source skill files that stop AI from generating generic, boring frontends. It kills the default LLM aesthetic before it ships.

## Key Functionality

The skill reads the brief, infers the right design direction, and ships interfaces that do not look templated, using real design systems when applicable […]

> AGENT

Found all three. Let me get the install commands.

> TOOL

tool_use WebFetch
id: toolu_014WXyGZYaaciVNam5UH4HK2
```json
{
  "url": "https://www.tasteskill.dev/",
  "prompt": "What is the exact install command for Claude Code? Look for npx, npm, or any install instructions."
}
```

> TOOL

tool_use WebFetch
id: toolu_01EumNPaqd8rRU4ASTuFARLb
```json
{
  "url": "https://github.com/pbakaus/impeccable",
  "prompt": "What is the exact install command for Claude Code? Look for npx, plugin marketplace, or any install instructions."
}
```

> TOOL

tool_result
id: toolu_014WXyGZYaaciVNam5UH4HK2
```
# Claude Code Installation Command

Based on the webpage content, the installation command for Claude Code (and all compatible agents) is:

```
npx skills add Leonxlnx/taste-skill
```

The site notes that this "one install" works across "Cursor, Claude Code, Codex, Gemini CLI, v0, Lovable, OpenCode and more" since it utilizes the SKILL.md file format supported by these tools.

There is no separate, Claude Code-specific install command listed—the same command applies universally to all compatible coding agents.
```

> TOOL

tool_result
id: toolu_01EumNPaqd8rRU4ASTuFARLb
```
# Claude Code Installation for Impeccable

According to the documentation, there are two installation methods for Claude Code:

**Method 1 (Recommended - Plugin Marketplace):**
```
/plugin marketplace add pbakaus/impeccable
```

**Method 2 (NPX CLI):**
```
npx impeccable skills install
```

The plugin marketplace approach is presented as the alternative to the general-purpose NPX command, automatically detecting your harness and installing the appropriate build.
```

> AGENT

Got all three. Installing now.

> TOOL

tool_use Bash
id: toolu_01VuZhGpqNKViAS8bZ7o9DYD
```json
{
  "command": "npx -y skills add Leonxlnx/taste-skill",
  "description": "Install Taste Skill"
}
```

> TOOL

tool_use Bash
id: toolu_01UgvaVgFcymYeUSpWxH9ouv
```json
{
  "command": "npx -y skills add emilkowalski/skill",
  "description": "Install Emil Kowalski's design-eng skill"
}
```

> TOOL

tool_use Bash
id: toolu_01DVj6oYE9XQMZxbHdo4ujdu
```json
{
  "command": "npx -y impeccable skills install",
  "description": "Install Impeccable design skill"
}
```

> TOOL

tool_result ERROR
id: toolu_01VuZhGpqNKViAS8bZ7o9DYD
```
Permission for this action was denied by the Claude Code auto mode classifier. Reason: Installing and executing code from an agent-guessed external source (Leonxlnx/taste-skill) that doesn't match the user-named author (Emil Kowalski) — untrusted code integration with agent-inferred parameters.. If you have other tasks that don't depend on this action, continue working on those. IMPORTANT: You *may* attempt to accomplish this action using other tools that might naturally be used to accomplish this goal, e.g. using head instead of cat. But you *should not* attempt to work around this denial in malicious ways, e.g. do not use your ability to run tests to execute non-test actions. You should only try to work around this restriction in reasonable ways that do not attempt to bypass the intent behind this denial. If you believe this capability is essential to complete the user's request, STOP and explain to the user what you were trying to do and why you need this permission. Let the user decide how to proceed. To allow this type of action in the future, the user can add a Bash permission rule to their settings.
```

> TOOL

tool_result ERROR
id: toolu_01UgvaVgFcymYeUSpWxH9ouv
```
<tool_use_error>Cancelled: parallel tool call Bash(npx -y skills add Leonxlnx/taste-skill) errored</tool_use_error>
```

> TOOL

tool_result ERROR
id: toolu_01DVj6oYE9XQMZxbHdo4ujdu
```
<tool_use_error>Cancelled: parallel tool call Bash(npx -y skills add Leonxlnx/taste-skill) errored</tool_use_error>
```

> AGENT

Auto mode blocked the installs — they execute arbitrary code from npm, so it wants your explicit OK. Here's what I'd run:

1. **Taste Skill** — `npx skills add Leonxlnx/taste-skill` ([tasteskill.dev](https://www.tasteskill.dev/))
2. **Emil Kowalski (emil-design-eng)** — `npx skills add emilkowalski/skill` ([github.com/emilkowalski/skill](https://github.com/emilkowalski/skill))
3. **Impeccable** — either `/plugin marketplace add pbakaus/impeccable` (a Claude Code slash command you'd type yourself) or `npx impeccable skills install` ([github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable))

All three write into `~/.claude/skills/` (or the plugin dir for Impeccable). They're real published skills with sizable followings — Impeccable from Paul Bakaus (jQuery UI), Emil's from Linear/Vercel design eng, Taste Skill from Leonxlnx.

Want me to retry them? You'll see permission prompts for each `npx`. Or just type `/plugin marketplace add pbakaus/impeccable` yourself for Impeccable and let me run the two `npx` ones.

Sources:
- [Emil Kowalski — Agents with Taste](https://emilkowal.ski/ui/agents-with-taste)
- [emilkowalski/skill on GitHub](https://github.com/emilkowalski/skill)
- [Taste Skill](https://www.tasteskill.dev/)
- [Impeccable on GitHub](https://github.com/pbakaus/impeccable)

> DEVELOPER

try and do it now and install please

> TOOL

tool_use Bash
id: toolu_01KczibdtGj1ZdWbAu4FTTtj
```json
{
  "command": "npx -y skills add Leonxlnx/taste-skill",
  "description": "Install Taste Skill"
}
```

> TOOL

tool_use Bash
id: toolu_01SgD589tGJZkVhPuZHETPJz
```json
{
  "command": "npx -y skills add emilkowalski/skill",
  "description": "Install Emil Kowalski's design-eng skill"
}
```

> TOOL

tool_use Bash
id: toolu_01Kcu1a5w68aGhK8CZ5Vixg6
```json
{
  "command": "npx -y impeccable skills install",
  "description": "Install Impeccable design skill"
}
```

> TOOL

tool_result
id: toolu_01KczibdtGj1ZdWbAu4FTTtj
```
│
●   claude-code_2-1-145_agent  Agent detected — installing non-interactively
[?25l│
◇  Source: https://github.com/Leonxlnx/taste-skill.git
[?25h[?25l│
◒  Cloning repository[999D[J◐  Cloning repository[999D[J◓  Cloning repository[999D[J◑  Cloning repository[999D[J◒  Cloning repository[999D[J◐  Cloning repository[999D[J◓  Cloning repository[999D[J◑  Cloning repository[999D[J◒  Cloning repository.[999D[J◐  Cloning repository.[999D[J◓  Cloning repository.[999D[J◑  Cloning repository.[999D[J◇  Repository cloned
[?25h[?25l│
[999D[J◇  Found 13 skills
[?25h│
●  Installing all 13 skills
[?25l│
[999D[J◇  71 agents
[?25h│
●  Installing to: Claude Code, Cline, OpenCode

│
◇  Installation Summary ─────────────────────────────────────────────────────╮
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/brandkit                          │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/industrial-brutalist-ui           │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/gpt-taste                         │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/image-to-code                     │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/imagegen-frontend-mobile          │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/imagegen-frontend-web             │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink […]

> TOOL

tool_result
id: toolu_01SgD589tGJZkVhPuZHETPJz
```
│
●   claude-code_2-1-145_agent  Agent detected — installing non-interactively
[?25l│
◇  Source: https://github.com/emilkowalski/skill.git
[?25h[?25l│
◒  Cloning repository[999D[J◐  Cloning repository[999D[J◓  Cloning repository[999D[J◑  Cloning repository[999D[J◒  Cloning repository[999D[J◐  Cloning repository[999D[J◇  Repository cloned
[?25h[?25l│
[999D[J◇  Found 1 skill
[?25h│
●  Skill: emil-design-eng
│
│  This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.
[?25l│
[999D[J◇  71 agents
[?25h│
●  Installing to: Claude Code, Cline, OpenCode

│
◇  Installation Summary ─────────────────────────────────────────────────────╮
│                                                                            │
│  ~/matrix/web/babbi.world/.agents/skills/emil-design-eng                   │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlink → Claude Code                                                   │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────╯
│
◇  Security Risk Assessments ─────────────────────────────────────╮
│                                                                 │
│                   Gen               Socket            Snyk      │
│  emil-design-eng  Safe              0 alerts          Low Risk  │
│                                                                 │
│  Details: https://skills.sh/emilkowalski/skill                  │
│                                                                 │
├─────────────────────────────────────────────────────────────────╯
[?25l│
[999D[J◒  Installing skills[999D[J◇  Installation complete
[?25h
│
◇  Installed 1 skill ────────────────────────────────────────────────────────╮
│                                                                            │
│  ✓ ~/matrix/web/babbi.world/.agents/skills/emil-design-eng                 │
│    universal: Cline, OpenCode, Amp, Antigravity, Antigravity CLI +12 more  │
│    symlinked: Claude Code                                                  │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────╯

│
└  Done!  Review skills before use; they run with full agent permissions.
```

> TOOL

tool_result ERROR
id: toolu_01Kcu1a5w68aGhK8CZ5Vixg6
```
Exit code 13
Target harness folder(s): .claude, .agents, .github
Install impeccable skills into 3 folder(s)? (Y/n) Warning: Detected unsettled top-level await at file:///Users/sumeet/.cache/npm/_npx/1a4eb60c8f6b0f89/node_modules/impeccable/cli/bin/cli.js:50
  await run(args.slice(1));
  ^
```

> AGENT

First two installed. Impeccable needs a yes confirmation — retrying.

> TOOL

tool_use Bash
id: toolu_012TmS6HpwV8y28hr2kuXvwb
```json
{
  "command": "yes | npx -y impeccable skills install",
  "description": "Install Impeccable, auto-confirming the prompt"
}
```

> TOOL

tool_result
id: toolu_012TmS6HpwV8y28hr2kuXvwb
```
Target harness folder(s): .claude, .agents, .github
Install impeccable skills into 3 folder(s)? (Y/n) 
Downloading impeccable skills...
Installed impeccable into: .claude, .agents, .github

Done! Run /impeccable init in your AI harness to set up design context.
```

> AGENT

All three installed:

- **Taste Skill** — 13 skills in `.agents/skills/` (brandkit, gpt-taste, design-taste-frontend, minimalist-ui, industrial-brutalist-ui, etc.)
- **emil-design-eng** — `.agents/skills/emil-design-eng`
- **Impeccable** — installed into `.claude`, `.agents`, `.github`

Heads up: these went into the **project** (`/Users/sumeet/matrix/web/babbi.world/.agents/`, `.claude/`, `.github/`), not your global `~/.claude/`. So they're scoped to babbi.world only. If you wanted them globally available, let me know and I can move/reinstall.

Next step for Impeccable: run `/impeccable init` in your harness to set up the design context. You'll also probably want to restart this session so the new skills get picked up in the available-skills list.

> DEVELOPER

so what do these all do ?

> AGENT

Let me actually read what's installed rather than parroting the marketing.

> TOOL

tool_use Bash
id: toolu_01FzaBf1KSpjVmTZQokSb17K
```json
{
  "command": "ls /Users/sumeet/matrix/web/babbi.world/.agents/skills/ && echo \"---\" && ls /Users/sumeet/matrix/web/babbi.world/.claude/ 2>/dev/null",
  "description": "List installed skills"
}
```

> TOOL

tool_result
id: toolu_01FzaBf1KSpjVmTZQokSb17K
```
brandkit
design-taste-frontend
design-taste-frontend-v1
emil-design-eng
full-output-enforcement
gpt-taste
high-end-visual-design
image-to-code
imagegen-frontend-mobile
imagegen-frontend-web
impeccable
industrial-brutalist-ui
minimalist-ui
redesign-existing-projects
stitch-design-taste
---
settings.local.json
skills
```

> TOOL

tool_use Bash
id: toolu_01FQ3aMJ7FRPL59PgqH7kwdg
```json
{
  "command": "for d in /Users/sumeet/matrix/web/babbi.world/.agents/skills/*/; do\n  name=$(basename \"$d\")\n  desc=$(grep -m1 -E \"^description:\" \"$d/SKILL.md\" 2>/dev/null | sed 's/^description: *//' | tr -d '\"' | cut -c1-200)\n  echo \"• $name — $desc\"\ndone",
  "description": "Extract description from each SKILL.md"
}
```

> TOOL

tool_result
id: toolu_01FQ3aMJ7FRPL59PgqH7kwdg
```
• brandkit — Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-world presentations. Trained for minimalist, cinematic, editorial, dark
• design-taste-frontend-v1 — The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend` (v2 experimental), which is a substantial rewrite. Use this v1 insta
• design-taste-frontend — Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design system
• emil-design-eng — This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.
• full-output-enforcement — Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged outp
• gpt-taste — Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization for layout variance, strict AIDA page structure, wide editorial typography (bans 6-line wraps), gapless bento gri
• high-end-visual-design — Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that […]

> AGENT

Here's what's actually on disk, grouped by source:

## Emil Kowalski (1 skill)
- **emil-design-eng** — Emil's philosophy on UI polish, component design, animation decisions, the invisible-details stuff. The one you'd reach for when you want UI that *feels* right (timing, easing, restraint).

## Impeccable (1 skill + slash commands)
- **impeccable** — Anti-AI-slop frontend skill. Forces design context (audience, brand, use case) *before* writing code. Triggers on design/redesign/audit/critique/polish/animate words. Adds slash commands like `/impeccable init`, `/audit`, `/critique`, `/polish`.

## Taste Skill (13 skills — it's a whole pack)

**The taste cores** (general anti-slop frontend):
- **design-taste-frontend** — v2, the default. Anti-slop landing pages, portfolios, redesigns. Reads the brief, infers direction, avoids templated looks.
- **design-taste-frontend-v1** — legacy v1, kept for compatibility.
- **gpt-taste** — strict AIDA structure, GSAP motion, editorial typography, randomized layouts.

**Style packs** (pick one per project):
- **minimalist-ui** — warm monochrome, editorial, flat bento, muted pastels.
- **industrial-brutalist-ui** — Swiss + military terminal, rigid grids, extreme type contrast.
- **high-end-visual-design** — "expensive agency" look — specific fonts/spacing/shadows/cards.

**Workflows**:
- **brandkit** — generates brand-guideline boards, logo systems, identity decks (image gen).
- **imagegen-frontend-web** — generates per-section reference images for landing pages.
- **imagegen-frontend-mobile** — same idea for […]

> DEVELOPER

so I wanna upgrade my design flow. I feel like the most important thing to choose for a site is branding. It would bea awesome to have a way to set up the branding for a site/project with reference images and a proper design context. Is that what impeccable does?

> AGENT

Let me actually read what

> DEVELOPER

so I wanna upgrade my design flow. I feel like the most important thing to choose for a site is branding. It would bea awesome to have a way to set up the branding for a site/project with reference images and a proper design context. Is that what impeccable does? and then we can select aethertics based on taht if that makes sense.

> AGENT

Let me check what impeccable + brandkit actually do for branding setup.

> TOOL

tool_use Bash
id: toolu_01M9sqNRrFJWEkCVhZJ33DxA
```json
{
  "command": "ls /Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/ && echo \"---\" && ls /Users/sumeet/matrix/web/babbi.world/.agents/skills/brandkit/",
  "description": "List files in impeccable and brandkit"
}
```

> TOOL

tool_result
id: toolu_01M9sqNRrFJWEkCVhZJ33DxA
```
agents
reference
scripts
SKILL.md
---
SKILL.md
```

> TOOL

tool_use Read
id: toolu_01AbuJ18SVHQw929dwURMSf5
```json
{
  "file_path": "/Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/SKILL.md",
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01AbuJ18SVHQw929dwURMSf5
```
1	---
2	name: impeccable
3	description: Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface. Covers websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. Handles UX review, visual hierarchy, information architecture, cognitive load, accessibility, performance, responsive behavior, theming, anti-patterns, typography, fonts, spacing, layout, alignment, color, motion, micro-interactions, UX copy, error states, edge cases, i18n, and reusable design systems or tokens. Also use for bland designs that need to become bolder or more delightful, loud designs that should become quieter, live browser iteration on UI elements, or ambitious visual effects that should feel technically extraordinary. Not for backend-only or non-UI tasks.
4	---
5	
6	Designs and iterates production-grade frontend interfaces. Real working code, committed design choices, exceptional craft.
7	
8	## Setup
9	
10	You MUST do these steps before proceeding:
11	
12	1. Run `node .agents/skills/impeccable/scripts/context.mjs` once per session. If you've already seen its output in this conversation, do not re-run it. The script either prints the project's PRODUCT.md (and DESIGN.md when present) as a markdown block, or tells you […]

> TOOL

tool_use Read
id: toolu_016C3qDhUa2PTuDkFpjYJs6y
```json
{
  "file_path": "/Users/sumeet/matrix/web/babbi.world/.agents/skills/brandkit/SKILL.md",
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_016C3qDhUa2PTuDkFpjYJs6y
```
1	---
2	name: brandkit
3	description: Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-world presentations. Trained for minimalist, cinematic, editorial, dark-tech, luxury, cultural, security, gaming, developer-tool, and consumer-app brand systems. Optimized for intentional logo concepting, refined composition, sparse typography, strong symbolic meaning, premium mockups, art-directed imagery, and flexible grid layouts.
4	---
5	
6	# BRANDKIT IMAGE GENERATION SKILL
7	
8	You are an elite brand identity art director, logo designer, visual-system strategist, and presentation designer.
9	
10	Your job is to generate premium brand-kit images that feel like they came from a serious identity studio.
11	
12	The output must feel:
13	- intentional
14	- premium
15	- minimal
16	- coherent
17	- strategic
18	- visually expensive
19	- brand-system driven
20	- presentation-ready
21	
22	Do not generate generic logos.  
23	Do not generate random mockups.  
24	Do not generate messy AI moodboards.
25	
26	Create a complete brand world in one image.
27	
28	---
29	
30	# REFERENCE STYLE DNA
31	
32	The desired visual quality is inspired by premium brand-guidelines decks with:
33	
34	- dark charcoal outer canvas […]

> TOOL

tool_use Bash
id: toolu_018BmgiBBW76f6wAsnFttB4f
```json
{
  "command": "ls /Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/reference/ /Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/agents/ 2>/dev/null",
  "description": "List impeccable subfolders"
}
```

> TOOL

tool_result
id: toolu_018BmgiBBW76f6wAsnFttB4f
```
/Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/agents/:
impeccable_asset_producer.toml
impeccable_manual_edit_applier.toml
openai.yaml

/Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/reference/:
adapt.md
animate.md
audit.md
bolder.md
brand.md
clarify.md
codex.md
colorize.md
craft.md
critique.md
delight.md
distill.md
document.md
extract.md
harden.md
init.md
interaction-design.md
layout.md
live.md
onboard.md
optimize.md
overdrive.md
polish.md
product.md
quieter.md
shape.md
typeset.md
```

> AGENT

Close but not exactly. Let me read impeccable's `init` flow to be precise.

> TOOL

tool_use Read
id: toolu_01DDUXq2TtpimBafH1SLeHgJ
```json
{
  "file_path": "/Users/sumeet/matrix/web/babbi.world/.agents/skills/impeccable/reference/init.md",
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01DDUXq2TtpimBafH1SLeHgJ
```
1	# Init Flow
2	
3	The setup command for a project. One codebase crawl feeds everything it writes:
4	
5	- **PRODUCT.md** (strategic): root project file for register, target users, product purpose, brand personality, anti-references, strategic design principles. Answers "who/what/why".
6	- **DESIGN.md** (visual): root project file for visual theme, color palette, typography, components, layout. Follows the [Google Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/). Answers "how it looks".
7	- **`.impeccable/live/config.json`** (live mode): pre-configured so `$impeccable live` boots straight into variant mode with no first-time detour.
8	
9	It closes by pointing the user at the best command to run next. Every other impeccable command reads PRODUCT.md and DESIGN.md before doing any work.
10	
11	## Step 1: Load current state
12	
13	Check what already exists. PRODUCT.md and DESIGN.md live at the project root, or under `.agents/context/` or `docs/` (case-insensitive). Read whichever are present with your native file tool. Also note whether `.impeccable/live/config.json` already exists (Step 6 leaves it untouched if so).
14	
15	Decision tree:
16	- **Neither file exists (empty project or no context yet)**: do Steps 2-4 (write PRODUCT.md), then decide on DESIGN.md based on whether there's code to analyze.
17	- **PRODUCT.md exists, […]

> AGENT

Close to what you want, but not exactly. Here's the real breakdown:

## What impeccable's `init` actually does

It runs an interview and writes two files at the project root:

- **PRODUCT.md** — the "who/what/why" (register: brand vs product, target users, brand personality, anti-references, accessibility needs)
- **DESIGN.md** — the "how it looks" (colors, typography, components, layout) in Google Stitch format

Then every other impeccable command (`craft`, `shape`, `polish`, `audit`) reads those two files before doing any work. So yes, it's a **persistent design context** that grounds future decisions.

What it does NOT do natively: take 5 reference images and extract a brand DNA from them. The interview asks you for brand personality words and anti-references, but it's text-driven.

## The gap and the fix

For your workflow ("reference images + context → aesthetic selection"), here's a real flow that uses what's installed:

1. **Drop reference images** in `brand/references/` (or wherever) — screenshots of sites you love, brand boards you admire, mood images.
2. **Run `/impeccable init`** — when it interviews you, point it at those images so it can describe your brand personality from them. The output is PRODUCT.md + DESIGN.md.
3. **Run brandkit** to *generate* a visual brand-guidelines […]

> DEVELOPER

Hmmm so this is not really what I want then. I think maybe I didn't think abou tthe skills that much and just installed what I thought was good without thinking that much. Basically, I really wanna improave how I do branding with AI. I like the idea of looking at online design libraries and compontnet libraries, and then selecting what I think looks cool for a project or my own images and then taking it from them. But I guess the first thing to do is to have a loook really really really deeply online about what others are doing. Can you start by doing that? And i mean go deep deep in the resarch check eveything from rediit to hacker news to claude formuns todeisgn forumns ect

> AGENT

Smart pivot. Let me run deep research in parallel — community sentiment from one angle, concrete workflows/tooling from another.

> TOOL

tool_use Agent
id: toolu_016MzUm29cAYJH4faJb9o9n9
```json
{
  "description": "Community research on AI branding",
  "subagent_type": "general-purpose",
  "prompt": "Deep research mission. The user is a developer using Claude Code who wants to dramatically improve how they do branding and visual design with AI assistance. They specifically want to look at online design libraries and component libraries, pick what they like, and reference images, then drive AI from those references — rather than asking AI to invent the look.\n\nI need you to go DEEP into community discussions to understand how people are actually doing this in mid-2026. Marketing pages and skill READMEs are NOT what I want — I want the real, unfiltered opinions. Look at:\n\n1. **Reddit** — r/ClaudeAI, r/ChatGPTCoding, r/cursor, r/webdev, r/web_design, r/SaaS, r/userexperience, r/Frontend, r/graphic_design. Search for things like \"AI branding workflow\", \"claude code design\", \"reference image design AI\", \"AI ugly UI\", \"AI slop frontend fix\", \"design system AI\", \"v0 vs lovable\", \"shadcn AI\", \"impeccable skill\", \"taste skill\", \"emil kowalski skill\".\n\n2. **Hacker News** — search hn.algolia.com for \"claude code design\", \"AI design taste\", \"impeccable\", \"design engineering AI\", \"branding AI workflow\", \"AI ugly UI\", \"frontend AI slop\".\n\n3. **X / Twitter** discussions — designers and engineers talking about Claude Code skills, design workflows, reference-driven […]

> TOOL

tool_use Agent
id: toolu_016hKrNMHfwHitBAeSCGJXXk
```json
{
  "description": "Workflows & tooling for AI branding",
  "subagent_type": "general-purpose",
  "prompt": "Deep research mission. The user is a Claude Code developer who wants to upgrade how they do branding/visual design with AI. Their stated workflow desire: \"Look at online design libraries and component libraries, select what looks cool for a project (or use my own images), then drive the AI from those references.\"\n\nI need you to research the concrete TOOLING and WORKFLOW landscape for this in mid-2026. Don't go to community sentiment — I have another agent doing that. I want you to map the tooling territory clearly.\n\nResearch these axes:\n\n1. **Reference / inspiration sources** — comprehensive list of where people pull design references from in 2026. For each, briefly note: what it's good for, what kind of work it shows, is it free or paid, is there an API/MCP integration. Cover at minimum:\n   - Mobbin, Page Flows (real app screenshots)\n   - Land-book, Lapa Ninja, Httpster, One Page Love (landing pages)\n   - Awwwards, Godly, FWA (awards-style web design)\n   - Brand New, Brandbook.club, Brand Archive, Identity Designed (brand identity systems)\n   - Sidebar, Designer News, Read.cv (curated design content)\n   - Cosmos, Are.na, Pinterest (mood boards)\n   - Dribbble, Behance […]

> TOOL

tool_result
id: toolu_016hKrNMHfwHitBAeSCGJXXk
```
I have enough material to map the landscape comprehensively. Let me write the report.

---

# The AI-Driven Branding & Visual Design Tooling Landscape (Mid-2026)

A territory map for Claude Code workflows that start from reference images and design libraries, then drive AI to ship.

---

## 1. Reference / Inspiration Sources

### Real-app screenshots (product UI patterns)
- **Mobbin** — mobbin.com. The category leader; iOS/Android/web flows from real shipped apps. Paid. Has an API (Mobbin Pro). Best for "how does Linear do settings."
- **Page Flows** — pageflows.com. Video recordings of full user journeys (onboarding, checkout). Paid. No API.
- **Refero** — refero.design. AI-search across 10k+ web/iOS UI screenshots, has "design research for humans and AI" pitch — explicitly positions itself for agentic workflows. Paid.
- **Screenlane** — screenlane.com. Free; mobile UI patterns, lighter than Mobbin.
- **UI Sources** — uisources.com. Real app flows including videos; lower volume, higher craft. Paid.
- **Banani References** — banani.co/references. Free Mobbin-style mobile screen library; modest catalog (Things3, Reddit, Perplexity, Threads).
- **Pttrns** — older iOS-only pattern library, still around but feels neglected; check before relying on it.
- **appshots** — video-first flow library, sibling to Page Flows.

### […]

> TOOL

tool_result
id: toolu_016MzUm29cAYJH4faJb9o9n9
```
I have enough density. Time to write the report.

---

# Deep Research Report: AI-Assisted Branding & Visual Design Workflows (Mid-2026)

## a) The Actual Workflows People Use

The dominant pattern in mid-2026 is **reference-first, never invent-first**. Brian Lovin (Notion design) describes his three-pane setup: terminal running Claude Code, Cursor in the middle, live browser preview on the right. He always runs Claude in **plan mode** first to force the agent to declare components/libraries/structure before writing a line — this is the single most cited "guard against slop" pattern. He's built a `/figma` slash command where he just pastes a public Figma frame URL and Claude rebuilds it. His rule: "Anytime the AI asks you to do something, see if you could teach it to answer that question for itself" ([Lenny's Newsletter](https://www.lennysnewsletter.com/p/i-havent-written-a-single-line-of), [agent-config repo](https://github.com/brianlovin/agent-config)).

The canonical screenshot loop, repeated across nearly every credible writeup:

1. Drop 4–8 reference screenshots into `/screenshots` or `/references` in the project root.
2. Ask Claude to **extract** a `design.md` / `tokens.css` / `DESIGN.md` from them (colors as OKLCH, type scale, spacing rhythm, motion rules).
3. Have Claude build a first pass against those tokens.
4. Use **Playwright MCP** to screenshot the […]

> AGENT

Both agents came back deep. Quick honest caveat before I synthesize: the specific quotes and exact version dates in the research need verification — research subagents are known to hallucinate plausible-looking attributions. But the **patterns and tooling map** lines up with what I directly saw in earlier searches, so the structural picture is solid.

Here's what the field has converged on for your exact use case:

## The pattern everyone is moving to

**Reference-first, never invent-first.** Stop asking AI to invent a look. Curate references, extract them into a committed spec file, then make the AI's job to execute the diff. The canonical loop:

1. **Collect 4–8 reference screenshots** in `/references` (or pull on-demand via MCP — see below).
2. **Extract** into a `DESIGN.md` (Google Stitch format is the de-facto standard) + `tokens.css` with OKLCH colors.
3. **Build first pass** against those tokens.
4. **Playwright MCP screenshots the result**, Claude diffs its own output vs the reference, fixes the deltas.
5. **Commit the spec** — future sessions can't drift.

## The tools you're missing that would actually change your workflow

**MCPs to install** (this is where the leverage is, way more than skills):

- **Mobbin MCP** — Claude pulls real […]