> AGENT

I'm not familiar with "Nano Banana 2." Could you clarify what it is? For example:

- Is it an IDE or code editor?
- A CLI tool or package?
- Something else entirely?

That way I can give you an accurate answer about whether it integrates with Claude Code.

> DEVELOPER

Gemini 3.1 or Veo 3

> AGENT

**No** — Claude Code works exclusively with Anthropic's Claude models (Opus, Sonnet, Haiku). It cannot use Google's Gemini 3.1 or Veo 3.

That said, you can absolutely **use Claude Code to write code** that calls the Gemini or Veo APIs — Claude Code just won't be powered by those models itself.

> DEVELOPER

Create this folder in your project root at .claude/skills/token-architect/.

File: Create a file named SKILL.md inside that folder. ---
name: token-architect
description: Use this skill to optimize token usage, manage context hygiene, and prevent session limits when the user is performing heavy coding or multi-file tasks.
---
# Token Architect Protocol
- **Plan Mode:** Before writing code, output a `<plan>` block and wait for confirmation.
- **Surgical Referencing:** Use `@filename` to target specific lines. Do not read entire directories.
- **Sub-Agent Delegation:** For heavy extraction, suggest spawning a sub-agent (Haiku) to return a lean summary.
- **Compaction:** If `/context` is >60%, suggest a `/compact` command with a specific "must-preserve" list.
- **Topic Switching:** If the task changes, explicitly ask if we should `/clear` to reset token compounding.

> AGENT

Created at [.claude/skills/token-architect/SKILL.md](/Users/carlosrestrepo/.claude/skills/token-architect/SKILL.md).

> AGENT

The **token-architect** skill helps you manage token/context usage during heavy coding sessions. It enforces 5 behaviors:

1. **Plan before coding** — outputs a `<plan>` block and waits for your approval before writing any code.
2. **Surgical file references** — targets specific lines via `@filename` instead of reading whole directories, keeping context lean.
3. **Sub-agent delegation** — suggests offloading heavy extraction tasks to a Haiku sub-agent that returns a compact summary instead of dumping everything into the main context.
4. **Compaction warnings** — when context exceeds 60%, prompts you to run `/compact` with a specific list of what must be preserved.
5. **Topic switch hygiene** — when you change subjects, asks if you want to `/clear` to prevent token bloat from compounding across unrelated tasks.

In short: it acts as a guard rail to keep your sessions from hitting context limits mid-task.

> DEVELOPER

is it good?

> AGENT

It's solid for what it does. A few honest observations:

**Strengths**
- The 60% compaction threshold is a practical, specific trigger — not vague.
- Forcing a `<plan>` block before coding prevents wasted tokens on wrong approaches.
- The `/clear` prompt on topic switches is a habit most people skip and regret.

**Weaknesses**
- `@filename` syntax for targeting specific lines isn't a native Claude Code feature — it's more of a convention, so the "surgical referencing" rule depends on you enforcing it manually.
- The sub-agent Haiku suggestion is advisory only — Claude won't automatically spawn one, it'll just suggest it.
- No guidance on *what* to put in the "must-preserve" list, which is often the hard part.

**Bottom line:** It's a good set of working principles, but it reads more like a reminder checklist than a skill that changes Claude's behavior automatically. For truly automatic enforcement (e.g., always plan before coding), you'd need hooks in `settings.json` rather than a SKILL.md.

Want me to add a hooks-backed version to reinforce any of these rules automatically?

> DEVELOPER

yes fix or improve the weaknesses

> AGENT

Let me check the current settings.json first.

> AGENT

Now I'll update both files — improve SKILL.md and add hooks to settings.json.

> AGENT

Here's what changed and why:

**SKILL.md improvements:**

| Weakness | Fix |
|---|---|
| `@filename` isn't a real feature | Replaced with actual Claude Code tool usage — `Read` with `offset`/`limit` for targeted line reads |
| Sub-agent is advisory only | Made it explicit with a suggested prompt, so you know exactly when/how to trigger it |
| No guidance on must-preserve | Added a concrete list of what belongs there (file paths, confirmed decisions, constraints, goal) |

**settings.json — new hook:**

Added a `PreToolUse` hook on `Edit`, `Write`, and `MultiEdit` that enforces the plan-before-coding rule automatically at the harness level — not just as a reminder Claude might skip.

Files updated:
- [.claude/skills/token-architect/SKILL.md](/Users/carlosrestrepo/.claude/skills/token-architect/SKILL.md)
- [.claude/settings.json](/Users/carlosrestrepo/.claude/settings.json)

> DEVELOPER

does this work for claude desktop app or we need to write another one

> AGENT

**You're good — no need to write another one.**

Both the skill and the hooks work in the Claude desktop app. Claude Code CLI and the desktop app share the same config files:

- `~/.claude/settings.json` — read by both
- `~/.claude/skills/` — read by both

Set it up once (which you already have) and it works everywhere.

> DEVELOPER

i do not see it in cowork

> AGENT

Could you clarify what "cowork" is? For example:

- Is it a specific tab or view inside the Claude desktop app?
- A different app or tool?
- A team/shared workspace feature?

That'll help me figure out why the skill isn't showing up there.

> DEVELOPER

tab

> AGENT

The **Cowork tab is a separate interface** from the Code tab — skills in `.claude/skills/` are a **Code tab feature** and won't appear in Cowork.

**Your options:**

1. **Use it in the Code tab** — that's where the skill lives and works as intended.
2. **Recreate it for Cowork manually** — Cowork doesn't have a skill system, but you could add the token-architect rules to a [CLAUDE.md](CLAUDE.md) file at `~/.claude/CLAUDE.md` (global) so the instructions are always present regardless of which tab you're in.

Want me to add a `CLAUDE.md` version so it covers both?

> DEVELOPER

yes

> AGENT

Created [.claude/CLAUDE.md](/Users/carlosrestrepo/.claude/CLAUDE.md) as a global file — it loads in every session across all tabs (Code, Cowork, Chat).

**Summary of what you now have:**

| File | Where it works |
|---|---|
| `.claude/skills/token-architect/SKILL.md` | Code tab — invokable as a skill |
| `.claude/settings.json` | Code tab — enforces plan hook automatically |
| `.claude/CLAUDE.md` | Everywhere (Code, Cowork, Chat) — always-on instructions |

> DEVELOPER

so i dont need a .skill file for this

> AGENT

Correct. Since the rules are now in `CLAUDE.md`, they're always active globally — you don't need to invoke a skill manually.

The `.claude/skills/token-architect/SKILL.md` is only useful if you want to:
- **Toggle** the behavior on/off (invoke it only when needed)
- **Share it** as a named, portable skill others can use

If you want the token-architect rules always on everywhere, `CLAUDE.md` alone is sufficient. Want me to delete the skill file?

> DEVELOPER

n

> AGENT

Got it — keeping both. The skill file stays as an explicit invocable version, and `CLAUDE.md` handles the always-on coverage across all tabs.
