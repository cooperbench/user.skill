> AGENT

Short answer: **not directly** — Claude Code (VS Code) and Claude Desktop are separate applications with different architectures.

Here's what's specific to each:

**Claude Code (VS Code)**
- Memory lives at `~/.claude/` (file-based, loaded by the CLI/extension)
- Skills are slash commands defined in your Claude Code config
- CLAUDE.md files are read by the Claude Code harness at runtime

**Claude Desktop**
- Has its own separate conversation history and project context
- Does not read `~/.claude/` memory files
- Does not support Claude Code skills/slash commands
- Has "Projects" with custom instructions, but those are entered manually in the UI

**What you *can* do manually:**
- Copy the contents of your CLAUDE.md (`~/.claude/CLAUDE.md`) into a Claude Desktop Project's custom instructions
- Paste relevant memory file contents as context at the start of a Desktop conversation

There's currently no automatic sync between the two. They don't share a common context layer.

> DEVELOPER

can you do it for me

> AGENT

The memory directory is empty, so there's nothing there to transfer. Your CLAUDE.md is already in my context.

I can compile the CLAUDE.md content (plus a summary of your skills) into a single block you can paste into a Claude Desktop **Project's custom instructions**. But I can't do it *for* you — Claude Desktop has no API or file-based config I can write to. You'd paste it manually.

Want me to generate that compiled block for you to copy-paste?

> DEVELOPER

y

> AGENT

Here's the block to paste into Claude Desktop → **Project settings → Custom instructions**:

---

```
## Token Architect Protocol
Apply these rules to optimize token usage and prevent context limits during heavy tasks.

### Plan Before Coding
Before writing or editing any code, output a <plan> block that includes:
- Files to be modified (with line ranges where possible)
- What will change and why
- Estimated scope: small / medium / large

Wait for explicit user confirmation before proceeding.

### Surgical Referencing
- Read only the relevant line ranges of a file — never load an entire file when a targeted read will do.
- Never scan a whole directory when a specific file path is known.
- When referencing code in responses, use `file_path:line_number` format.

### Sub-Agent Delegation
When a task requires extracting or summarizing content across 3+ files, suggest:
> "This looks like a good candidate for a sub-agent to return a lean summary. Want me to spawn one?"

Do not dump full file contents into context to answer something a targeted search could handle.

### Compaction
When the conversation has grown long, proactively suggest compacting. Must-preserve list should include:
- Active file paths and their purpose
- Decisions already confirmed by the user
- Constraints or requirements stated by the user
- Current task goal in one sentence

### Topic Switching
If the request shifts to a clearly different task or codebase area, ask once:
> "This looks like a new topic. Should we clear context to avoid token compounding from the previous task?"

## User Context
- Works on Remotion (video-in-React framework) — docs, demos, sfx, experts page, web renderer
- Does AI-assisted video editing (talking-head cuts, subtitles, ffmpeg pipelines)
- Builds business offers and niche-finding workflows for solo AI creators
- Uses Google NotebookLM programmatically
- Prefers terse, direct responses — no filler, no trailing summaries
```

---

**To apply:** Open Claude Desktop → create or open a Project → click the project name → **Edit instructions** → paste the above.

The slash commands (skills) themselves won't work in Desktop since it has no skill runner, but the behavioral rules and your work context will carry over.

> DEVELOPER

is this specific for each project or in general for all

> AGENT

In Claude Desktop, **Project custom instructions are per-project** — each project has its own separate instructions.

For **global** behavior across all conversations (outside of any project), Claude Desktop doesn't currently have a global custom instructions setting the way Claude Code's `~/.claude/CLAUDE.md` works.

So your options:
- **Per-project**: paste into each project you create
- **Workaround for "global"**: create a default project you always use, or manually add the instructions to each new project

> DEVELOPER

Audifono

> AGENT

No entiendo — ¿qué quieres decir con "Audifono"? ¿Es el nombre de un proyecto en Claude Desktop?

> DEVELOPER

olvidar

> AGENT

Entendido, olvidado.
