> DEVELOPER

Looking at hermes in ~/code/hermes-agent I see it comes with tons of skills already, the loader shows:

██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗       █████╗  ██████╗ ███████╗███╗   ██╗████████╗
██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝      ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗█████╗███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║
██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║╚════╝██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║
██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║      ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝      ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝

╭──────────────────────────── Hermes Agent v0.10.0 (2026.4.16) · upstream 9f22977f ─────────────────────────────╮
│                                   Available Tools                                                             │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⣀⣀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   browser: browser_back, browser_cdp, browser_click, ...                      │
│  ⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣇⠸⣿⣿⠇⣸⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀   clarify: clarify                                                            │
│  ⠀⢀⣠⣴⣶⠿⠋⣩⡿⣿⡿⠻⣿⡇⢠⡄⢸⣿⠟⢿⣿⢿⣍⠙⠿⣶⣦⣄⡀⠀   code_execution: execute_code                                                │
│  ⠀⠀⠉⠉⠁⠶⠟⠋⠀⠉⠀⢀⣈⣁⡈⢁⣈⣁⡀⠀⠉⠀⠙⠻⠶⠈⠉⠉⠀⠀   cronjob: cronjob                                                            │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠛⢁⡈⠛⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   delegation: delegate_task                                                   │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣦⣤⣈⠁⢠⣴⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   discord: discord_server                                                     │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⢿⣿⣦⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   file: patch, read_file, search_files, write_file                            │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣦⣈⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   homeassistant: ha_call_service, ha_get_state, ...                           │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⠦⠈⠙⠿⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   (and 12 more toolsets...)                                                   │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣤⡈⠁⢤⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                               │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   Available Skills                                                            │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠑⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   autonomous-ai-agents: claude-code, codex, hermes-agent, opencode            │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⢰⡆⠈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   creative: architecture-diagram, ascii-art, ascii-video, b...                │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠈⣡⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   data-science: jupyter-live-kernel                                           │
│  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   devops: webhook-subscriptions                                               │
│                                   email: himalaya                                                             │
│  claude-opus-4.6 · Nous Research  gaming: minecraft-modpack-server, pokemon-player                            │
│               /root               general: dogfood                                                            │
│  Session: 20260420_113745_966d4d  github: codebase-inspection, github-auth, github-code-r...                  │
│                                   mcp: native-mcp                                                             │
│                                   media: gif-search, heartmula, songsee, […]

> AGENT

Let me explore both codebases to understand how Hermes skills work and how Moltis currently handles tools/skills.

> TOOL

tool_use Agent
id: toolu_017QrLwWgj3d4WR17RwrLs2d
```json
{
  "subagent_type": "Explore",
  "description": "Explore Hermes Agent skills system",
  "prompt": "Thoroughly explore ~/code/hermes-agent to understand how skills work. I need to understand:\n\n1. How skills are defined (file format, metadata, structure)\n2. How skills are loaded and discovered\n3. How skills are invoked/executed at runtime\n4. The relationship between skills and tools\n5. Look at a few concrete skill examples (e.g. from research/, creative/, productivity/ categories)\n6. How the skill registry/loader works\n7. Any skill configuration or manifest files\n\nFocus on the skill system architecture. Look at directories like skills/, src/skills/, or similar. Check package.json or pyproject.toml for the project type. Be very thorough — check multiple directories and naming conventions."
}
```

> TOOL

tool_result
id: toolu_017QrLwWgj3d4WR17RwrLs2d
```
Perfect! Now I have all the information I need. Let me compile a comprehensive report on the Hermes Agent skills system.

## Comprehensive Report: Hermes Agent Skills System Architecture

Based on my thorough exploration of the hermes-agent codebase, here's a complete understanding of how the skills system works:

### 1. **Skill Definition & File Format**

Skills are defined as **SKILL.md files** with YAML frontmatter and markdown body content. The format follows agentskills.io standards for compatibility.

**Location:** `~/.hermes/skills/` (configurable with external skill dirs)

**File Structure:**
```
skills/
├── creative/
│   ├── ascii-art/
│   │   └── SKILL.md          # Main skill file
│   ├── p5js/
│   │   ├── SKILL.md
│   │   ├── references/       # Supporting documentation
│   │   ├── templates/        # Output templates
│   │   ├── scripts/          # Executable scripts
│   │   └── assets/           # Supplementary files
└── research/
    ├── arxiv/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── search_arxiv.py
```

**SKILL.md Frontmatter Format:**
```yaml
---
name: arxiv                                    # Required, max 64 chars
description: Search arXiv papers...           # Required, max 1024 chars
version: 1.0.0                                # Optional
author: Hermes Agent                          # Optional
license: MIT                                  # Optional (agentskills.io)
platforms: [macos, linux]                     # Optional: restrict to OS platforms
prerequisites:                                # Optional: legacy […]

> TOOL

tool_use Agent
id: toolu_01BowMCPkb6tR2axcGAcurGu
```json
{
  "subagent_type": "Explore",
  "description": "Explore Moltis tools/skills system",
  "prompt": "Thoroughly explore the Moltis codebase to understand how the agent/tools system works. Focus on:\n\n1. How tools are defined and registered (look in crates/tools/, crates/agents/)\n2. How tools are dispatched/executed at runtime\n3. The tool schema format (JSON schema for tool parameters)\n4. How the agent loop uses tools (crates/agents/src/runner.rs)\n5. Any existing \"skill\" or \"prompt template\" concept\n6. How the system prompt is constructed\n7. The ToolRegistry or similar pattern\n8. How tool results are fed back to the LLM\n\nThis is a Rust workspace. Be very thorough."
}
```

> TOOL

tool_result
id: toolu_01BowMCPkb6tR2axcGAcurGu
```
Now let me output my comprehensive findings:

## Comprehensive Moltis Agent/Tools System Architecture

Based on my thorough exploration of the Moltis codebase, here's the complete understanding of how the agent/tools system works:

---

### 1. **Tool Definition & Registration**

#### Core Trait: `AgentTool` (crates/agents/src/tool_registry.rs)
```rust
#[async_trait]
pub trait AgentTool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn parameters_schema(&self) -> serde_json::Value;  // JSON Schema
    async fn warmup(&self) -> Result<()> { Ok(()) }    // Optional init hook
    async fn execute(&self, params: serde_json::Value) -> Result<serde_json::Value>;
}
```

**All tools implement this trait**, including:
- Built-in tools (exec, calc, browser, web_fetch, web_search, etc.) — crates/tools/src/
- Skill management tools (create_skill, update_skill, read_skill, delete_skill) — crates/tools/src/skill_tools.rs
- Memory tools (memory_save, memory_forget, etc.) — crates/chat/src/memory_tools.rs
- Session communication tools (send_message_to_session) — crates/tools/src/sessions_communicate.rs
- MCP-sourced tools — dynamically registered from Model Context Protocol servers

**Key Implementation Pattern (e.g., CalcTool)**:
```rust
pub struct CalcTool;

#[async_trait]
impl AgentTool for CalcTool {
    fn name(&self) -> &str { "calc" }
    fn description(&self) -> &str { "Evaluate arithmetic expressions..." }
    fn parameters_schema(&self) -> Value {
        json!({
            "type": "object",
            "required": ["expression"],
            "properties": { "expression": { "type": "string", ... } }
        })
    }
    async fn […]

> AGENT

Now I have a clear picture of both systems. Here's the good news: **Moltis already has a skill system** (`crates/skills/`) that uses the same SKILL.md format as Hermes. The architecture is already there — what's missing is bundled default content.

## Recommended Approach

**Embed default skills in the binary** (same pattern as web UI assets with `include_dir!`), and add a "bundled" discovery source to the existing skill system.

### Concretely, three changes:

**1. New crate: `crates/default-skills/`**
- Contains a `skills/` directory tree with ported SKILL.md files from Hermes
- Uses `include_dir!` to embed them at compile time
- Exposes a function like `fn bundled_skills() -> &'static IncludeDir` or an iterator over `(name, metadata, content)`
- Binary size impact is small — these are just markdown files

**2. Extend skill discovery** (`crates/skills/src/discover.rs`)
- Add a 5th source after the existing four (project → personal → registry → plugin → **bundled**)
- Bundled skills are lowest priority — anything the user creates overrides them
- No filesystem extraction needed; serve directly from memory

**3. Port the Hermes skills**
- Map Hermes tool references to Moltis tool names (`terminal` → `exec`, `web_extract` → `web_fetch`, `files` → relevant Moltis tools)
- Drop skills that […]