> DEVELOPER

Do we have the newest version of claude code installed?

> TOOL

tool_use Bash
id: toolu_01JtirX1NDGnWpnJuuXVdwpc
```json
{
  "command": "claude --version 2>/dev/null || echo \"claude command not found\"",
  "description": "Check installed Claude Code version"
}
```

> TOOL

tool_use WebSearch
id: toolu_01G99iVC8cKeM8CfRCkb5u7c
```json
{
  "query": "Claude Code latest version release April 2026"
}
```

> TOOL

tool_result
id: toolu_01JtirX1NDGnWpnJuuXVdwpc
```
2.1.105 (Claude Code)
```

> TOOL

tool_result
id: toolu_01G99iVC8cKeM8CfRCkb5u7c
```
Web search results for query: "Claude Code latest version release April 2026"

Links: [{"title":"Releases · anthropics/claude-code","url":"https://github.com/anthropics/claude-code/releases"},{"title":"What's new - Claude Code Docs","url":"https://code.claude.com/docs/en/whats-new"},{"title":"Claude Code by Anthropic - Release Notes - April 2026 Latest Updates - Releasebot","url":"https://releasebot.io/updates/anthropic/claude-code"},{"title":"Release notes | Claude Help Center","url":"https://support.claude.com/en/articles/12138966-release-notes"},{"title":"Claude Platform - Claude API Docs","url":"https://platform.claude.com/docs/en/release-notes/overview"},{"title":"Anthropic Release Notes - April 2026 Latest Updates - Releasebot","url":"https://releasebot.io/updates/anthropic"},{"title":"Claude Code Changelog: All Release Notes (2026)","url":"https://claudefa.st/blog/guide/changelog"},{"title":"Claude by Anthropic - Release Notes - April 2026 Latest Updates - Releasebot","url":"https://releasebot.io/updates/anthropic/claude"},{"title":"Decoding the Claude Code April 2026 Changelog: A Comprehensive Overview of 30+ Version Iterations from 2.1.69 to 2.1.101 - Apiyi.com Blog","url":"https://help.apiyi.com/en/claude-code-changelog-2026-april-updates-en.html"},{"title":"ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices","url":"https://claudelog.com/claude-code-changelog/"}]

Here's a summary of the latest Claude Code releases as of April 2026:

## Claude Code — Latest Version Updates (April 2026)

Anthropic's Claude Code entered its most intensive iteration cycle ever between March and April 2026, pushing from **v2.1.69 to v2.1.101** in just five weeks.

### Key Highlights

**Model Support:**
- Claude Opus 4.7 xhigh is now available!
- Auto mode is now available for Max subscribers when using Opus 4.7. An xhigh effort level was added for Opus 4.7, sitting between high and max.
- Claude Opus 4.7 is described as Anthropic's most capable […]

> AGENT

You're on **Claude Code v2.1.105**, which is quite recent but there have been updates beyond that. Let me check what the absolute latest is.

> TOOL

tool_use WebFetch
id: toolu_015dQmqLeDhf9uk2VqDLfFuM
```json
{
  "url": "https://github.com/anthropics/claude-code/releases",
  "prompt": "What is the very latest release version number of Claude Code? List the most recent 3-5 releases with their version numbers and dates."
}
```

> TOOL

tool_result
id: toolu_015dQmqLeDhf9uk2VqDLfFuM
```
# Latest Claude Code Releases

## Most Recent Version
**v2.1.112** - Released April 16, 2024

## Latest 5 Releases

1. **v2.1.112** (April 16, 19:55)
   - Fixed "claude-opus-4-7 is temporarily unavailable" for auto mode

2. **v2.1.111** (April 16, 15:18)
   - Claude Opus 4.7 xhigh now available with `/effort` tuning
   - Auto mode available for Max subscribers
   - Added `/ultrareview` for comprehensive code review
   - Windows PowerShell tool progressively rolling out
   - Multiple UI and performance improvements

3. **v2.1.110** (April 15, 22:07)
   - Added `/tui` command for flicker-free fullscreen rendering
   - Added push notification tool
   - Improved plugin management and MCP server handling
   - Various bug fixes and performance improvements

4. **v2.1.109** (April 15, 04:02)
   - Improved the extended-thinking indicator with rotating progress hint

5. **v2.1.108** (April 14, 19:12)
   - Added prompt caching options (`ENABLE_PROMPT_CACHING_1H`)
   - Added recap feature for session context
   - Model can now discover built-in slash commands via Skill tool
   - Various fixes for memory and performance
```

> AGENT

You're on **v2.1.105**, and the latest is **v2.1.112** (released yesterday, April 16). You're 7 patch versions behind. Here's what you'd pick up by updating:

| Version | Highlights |
|---------|-----------|
| **2.1.112** | Fix for "claude-opus-4-7 is temporarily unavailable" in auto mode |
| **2.1.111** | **Claude Opus 4.7 xhigh**, `/ultrareview`, auto mode for Max subscribers |
| **2.1.110** | `/tui` fullscreen mode, push notifications |
| **2.1.109** | Improved extended-thinking progress indicator |
| **2.1.108** | 1-hour prompt caching option, session recap, built-in skill discovery |

The big headline is **Opus 4.7** support and the new `/ultrareview` command for parallel multi-agent code review.

To update, run:

```bash
claude update
```

or if you installed via npm:

```bash
npm install -g @anthropic-ai/claude-code@latest
```

`★ Insight ─────────────────────────────────────`
- **Opus 4.7 vs 4.6**: Opus 4.7 adds an `xhigh` effort level (between `high` and `max`) and is described as Anthropic's most capable model for complex reasoning and agentic coding — same pricing as 4.6 ($5/$25 per MTok).
- **Deprecation notice**: Claude Sonnet 4 and Claude Opus 4 (the non-4.5/4.6 variants) are being retired on **June 15, 2026**. Migrate to 4.6+ models.
- **`/ultrareview`** runs comprehensive code review in the cloud using parallel multi-agent […]

> DEVELOPER

Can you do it?

> TOOL

tool_use Bash
id: toolu_01B63dyRc6p3T34uMqdnXsqK
```json
{
  "command": "claude update 2>&1",
  "description": "Update Claude Code to latest version",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01B63dyRc6p3T34uMqdnXsqK
```
Current version: 2.1.105
Checking for updates to latest version...

Warning: Multiple installations found
- npm-global at /home/<USER>/.linuxbrew/bin/claude (currently running)
- native at /home/<USER>/.local/bin/claude
New version available: 2.1.112 (current: 2.1.105)
Installing update...
Using global installation update method...
Successfully updated from 2.1.105 to version 2.1.112
```

> AGENT

Successfully updated from **v2.1.105 → v2.1.112**.

One thing to note — the updater flagged **two installations**:

| Installation | Path |
|---|---|
| **npm-global** (active) | `/home/<USER>/.linuxbrew/bin/claude` |
| **native** | `/home/<USER>/.local/bin/claude` |

The npm-global one (Linuxbrew) is the one that was updated and is currently running. You may want to update or remove the native one at `~/.local/bin/claude` to avoid version confusion down the road.

`★ Insight ─────────────────────────────────────`
- **Dual installations** can cause subtle issues — whichever is first on your `$PATH` wins. If you switch shells or change PATH ordering, you could silently drop back to the older version.
- The new session will pick up Opus 4.7 support, `/ultrareview`, `/tui` fullscreen mode, and the 1-hour prompt caching option. You'll need to **restart this session** (exit and re-launch `claude`) to use the new version.
`─────────────────────────────────────────────────`