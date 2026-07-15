> DEVELOPER

I think something like this is miising from out opencode installation? https://github.com/obra/superpowers/blob/main/.opencode/plugins/superpowers.js

> AGENT

Let me explore the codebase and fetch that URL to understand what's missing.

> AGENT

Now let me look at our current OpenCode setup and the using-superpowers skill to understand what we'd need to adapt.

> AGENT

Now I have a clear picture. Let me invoke the brainstorming skill since this involves creating new functionality.

> AGENT

Using brainstorming to design the OpenCode plugin. I've already explored the project context. Here's what I found: **Current state:** - `obra/superpowers` has `.opencode/plugins/superpowers.js` — a runtime JS plugin that auto-registers skills and injects bootstrap context into OpenCode sessions - Our repo (`entireio/skills`) only has `.opencode/INSTALL.md` — documentation telling users to add a git URL to their config, but **no actual plugin entry point** that OpenCode would execute - Our three skills live in `plugins/entire/skills/` (explain, search, session-handoff) - All our other tool integrations (Claude Code, Codex, Cursor, Gemini) are JSON-manifest-based with no JS plugins The superpowers plugin does two things: 1. **Config hook** — registers the skills directory so OpenCode discovers skills automatically 2. **Message transform** — injects `using-superpowers` bootstrap content into the first user message of each session (with tool name mapping) Let me start with my first clarifying question. The superpowers plugin has two distinct behaviors: (a) auto-registering the skills directory, and (b) injecting bootstrap context from the `using-superpowers` skill into every session. For our `entire` plugin: - **(a)** makes clear sense — register `plugins/entire/skills` so OpenCode finds our skills - **(b)** is superpowers-specific — it injects the `using-superpowers` SKILL.md content, which is their onboarding/meta-skill **Do we need any bootstrap injection for our plugin?** Our skills (explain, search, session-handoff) are task-specific and invoked on demand — they don't seem to need session-start injection like superpowers does. Should our plugin be config-only (just register the skills path), or is there context we should inject into OpenCode sessions too?

> DEVELOPER

would entire benefit from a using-entire skill similar to b?

> AGENT

Good question. Let me think about this in terms of what it would actually buy us. **The case for a `using-entire` bootstrap:** Our skills are most valuable when used *proactively* — the agent should reach for `entire search` when someone asks "what did we work on last week?" or `entire explain` when they're puzzled by unfamiliar code. Without bootstrap context, the agent only knows the one-line descriptions from the skill list. A bootstrap could establish: - When to proactively use each skill (not just on explicit request) - How the skills relate to Entire's checkpoint/session system - Tool name mapping for OpenCode **The case against:** - We only have 3 skills — `using-superpowers` exists because superpowers has dozens of skills with a complex workflow (brainstorming → planning → TDD → etc). Our skills are straightforward and self-descriptive. - The skill descriptions already appear in system reminders. An agent that sees "Use when the user wants to find prior work, checkpoints, or agent conversations" doesn't need much more guidance. - Bootstrap injection adds token cost to every single session, even ones that never touch Entire features. **My recommendation:** Not yet. The ROI is low with only 3 focused skills. If we grow to 6+ skills or find that agents aren't using them proactively, then it becomes worth it. For now, the plugin should just handle **(a)** — auto-registering the skills path — which is the piece that's actually missing and blocking OpenCode from discovering our skills at all. Does that reasoning track, or do you see proactive usage as a bigger problem than I'm giving it credit for?

> DEVELOPER

okay can you just do a then

> AGENT

Straightforward — create an OpenCode plugin JS file that registers our skills directory. Let me write the plan.

> AGENT

Let me create the plugin file and update the install docs.

> AGENT

Now let me verify the path resolution is correct.

> AGENT

Path resolves correctly to `plugins/entire/skills` which contains all three skills (explain, search, session-handoff). Done. Two changes: 1. **Created** `.opencode/plugins/entire.js` — minimal plugin that auto-registers the `plugins/entire/skills` directory via OpenCode's `config` hook 2. **Updated** `.opencode/INSTALL.md` — mentions the plugin handles skills registration automatically

> DEVELOPER

commit and push

> AGENT

Committed and pushed. The three changes (new plugin file, updated INSTALL.md, updated README.md) are live on main.

> DEVELOPER

explain this for opencode plugin superpowers@git+https://github.com/obra/superpowers.git

> AGENT

The explain skill traces code to git commits/session transcripts — not quite what's needed here. Let me just explain this directly. `superpowers@git+https://github.com/obra/superpowers.git` is an **OpenCode plugin reference** that goes in your OpenCode config file. Here's how it breaks down: | Part | Meaning | |------|---------| | `superpowers` | The plugin name (used for display and deduplication) | | `@` | Separator between name and source | | `git+` | Protocol prefix — tells OpenCode to clone from a git repo | | `https://github.com/obra/superpowers.git` | The repo URL to clone | When OpenCode starts, it: 1. **Clones** the repo (or uses a cached copy) 2. **Finds** `.opencode/plugins/superpowers.js` — the plugin entry point 3. **Calls** the exported `SuperpowersPlugin` function, which returns hooks 4. **Runs the `config` hook** — this pushes the `skills/` directory onto `config.skills.paths`, so OpenCode discovers all superpowers skills automatically 5. **Runs the `messages.transform` hook** — this injects the `using-superpowers` bootstrap content into the first user message of each session It's the same pattern as our `skills@git+https://github.com/entireio/skills.git` — except superpowers also does the bootstrap injection (step 5), while our plugin only does skills registration (step 4). You'd add it to your OpenCode config alongside ours if you wanted both: ```json { "plugin": [ "skills@git+https://github.com/entireio/skills.git", "superpowers@git+https://github.com/obra/superpowers.git" ] } ```

> DEVELOPER

I don't see the entire commands in opencode

> AGENT

Let me check if we're missing something that tells OpenCode where to find the plugin entry point.

> AGENT

That's the missing piece. Superpowers has a **`package.json`** at the repo root with: ```json { "name": "superpowers", "version": "5.0.7", "type": "module", "main": ".opencode/plugins/superpowers.js" } ``` The `main` field tells OpenCode which JS file to load as the plugin entry point. We don't have a `package.json` — OpenCode has no way to find our `.opencode/plugins/entire.js`.

> AGENT

Confirmed — no `package.json` exists. Let me add one.

> AGENT

Pushed. The issue was that OpenCode uses the `main` field in `package.json` to find the plugin entry point. Without it, our `.opencode/plugins/entire.js` was never loaded. Try restarting OpenCode — the Entire skills (explain, search, session-handoff) should now be discoverable.
