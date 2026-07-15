> DEVELOPER

you're on a PR right now that refactored the agent hook system to make it easier to add new agents. This is the PR: https://github.com/entireio/cli/pull/360. I want to add in support for codex from openai, here is the documentation:https://developers.openai.com/codex/changelog/?type=codex-cli. They mention hooks in this change log: https://developers.openai.com/codex/changelog/?type=codex-cli. Search to see if the hooks are ready to implement and what state they're in.

> AGENT

I'll research the Codex CLI hooks documentation to understand what's available. Let me fetch the documentation and PR details in parallel.

> TOOL

tool_use Task
id: toolu_011GehfbVRV44vJ93forvcR4
```json
{
  "description": "Research Codex CLI hooks",
  "prompt": "Research the OpenAI Codex CLI hooks system. I need to understand:\n1. What hooks does Codex CLI support?\n2. What is the hook format/protocol?\n3. Are hooks stable/released or still experimental?\n\nFetch these URLs and extract all relevant information about hooks:\n- https://developers.openai.com/codex/changelog/?type=codex-cli - Look for hook-related changelog entries\n- https://developers.openai.com/codex/overview - General overview\n- https://developers.openai.com/codex/hooks - Direct hooks documentation (if it exists)\n\nAlso search the web for \"OpenAI Codex CLI hooks\" to find any additional documentation, blog posts, or GitHub issues about the hooks system.\n\nReturn a comprehensive summary of what hooks are available, their format, and their maturity level.",
  "subagent_type": "general-purpose"
}
```

> TOOL

tool_use Bash
id: toolu_01PiBnFcEe9RNuXNuXax7n8G
```json
{
  "command": "gh pr view 360 --json title,body,files 2>/dev/null | head -200",
  "description": "Get PR 360 details"
}
```

> TOOL

tool_use Task
id: toolu_015kEQQ9ad7tmd7TbkBmhaBx
```json
{
  "description": "Explore hook registry codebase",
  "prompt": "Explore the codebase at /Users/evisdrenova/code/entire/devenv/cli to understand the current agent hook system architecture. Specifically:\n\n1. Read the hook_registry.go file that was opened by the user\n2. Find all agent-related files in cmd/entire/cli/ - look for files related to hooks, agents, and the registry pattern\n3. Understand how existing agents (like Claude Code) are registered and what hooks they implement\n4. Look at the current branch (add_codex_support) for any existing work\n\nBe thorough - look at all relevant files to understand the full hook/agent registration system.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_011GehfbVRV44vJ93forvcR4
```
I now have enough information to compile a comprehensive summary. Here is what I found:

---

## Comprehensive Summary: OpenAI Codex CLI Hooks System

### 1. Current Shipped State: The `notify` System

The only **officially documented and released** hook mechanism in Codex CLI is the **`notify`** configuration. This is documented in the official [Advanced Configuration](https://developers.openai.com/codex/config-advanced/) and [Configuration Reference](https://developers.openai.com/codex/config-reference/) pages.

**Configuration format** (in `~/.codex/config.toml` or `.codex/config.toml`):

```toml
notify = ["python3", "/path/to/notify.py"]
```

**Supported event:** Currently only one event type:
- `agent-turn-complete` -- fired when the agent finishes a turn

**Protocol:** The external program receives a **single JSON argument** (passed as `sys.argv[1]`, not stdin) with this payload structure:

| Field | Description |
|-------|-------------|
| `type` | Event identifier (e.g., `agent-turn-complete`) |
| `thread-id` | Session identifier |
| `turn-id` | Turn identifier |
| `cwd` | Current working directory |
| `input-messages` | Array of user messages that triggered the turn |
| `last-assistant-message` | Final assistant response text |

**Example handler** from the official docs:

```python
#!/usr/bin/env python3
import json, subprocess, sys

def main() -> int:
    notification = json.loads(sys.argv[1])
    if notification.get("type") != "agent-turn-complete":
        return 0
    title = f"Codex: {notification.get('last-assistant-message')}"
    message = " ".join(notification.get("input-messages", []))
    subprocess.check_output([
        "terminal-notifier", […]

> TOOL

tool_result
id: toolu_01PiBnFcEe9RNuXNuXax7n8G
```

```

> TOOL

tool_result
id: toolu_015kEQQ9ad7tmd7TbkBmhaBx
```
Excellent! Now I have a comprehensive understanding of the system. Let me create a summary report.

## Summary: Agent Hook System Architecture

Based on my thorough exploration of the codebase, here's a complete overview of the current agent hook system architecture:

### Core Architecture Overview

The system is built on a **registry pattern** that separates agent definitions from hook handler implementations to avoid circular dependencies. The architecture consists of several key layers:

#### 1. **Agent Interface & Registry** (`cmd/entire/cli/agent/`)

**Agent Interface** (`agent.go`):
- `Agent` - Base interface all agents must implement with methods like:
  - `Name()` (registry key, e.g., "claude-code")
  - `Type()` (display name, e.g., "Claude Code")
  - `Description()` 
  - `DetectPresence()` - checks if agent is configured
  - `GetHookConfigPath()` - location of hooks config
  - `SupportsHooks()` - boolean flag
  - Session management: `ParseHookInput()`, `ReadSession()`, `WriteSession()`, `FormatResumeCommand()`
  - Protected dirs, session storage paths

**Optional Interfaces**:
- `HookSupport` - Implements: `InstallHooks()`, `UninstallHooks()`, `AreHooksInstalled()`, `GetSupportedHooks()`
- `HookHandler` - Implements: `GetHookNames()` - returns list of hook verbs the agent supports
- `FileWatcher` - For agents without hook support (Aider, etc.)
- `TranscriptAnalyzer` - Agents providing transcript analysis
- `TranscriptChunker` - Agents supporting transcript chunking

**Registry** (`registry.go`):
```go
var registry = […]

> AGENT

Here's what I found:

## Codex CLI Hooks - Current State

**TL;DR: The hooks are NOT ready for a full integration.** The only stable, documented hook is extremely limited.

### What's Available (Stable)

The only publicly exposed hook is **`notify`** — a one-way, fire-and-forget notification with a single event type:

- **Event:** `agent-turn-complete` (fires when the agent finishes a turn)
- **Protocol:** Spawns an external command with JSON passed as **`sys.argv[1]`** (command-line argument, not stdin)
- **Config location:** `~/.codex/config.toml` or `.codex/config.toml`
- **Config format:**
  ```toml
  notify = ["python3", "/path/to/script.py"]
  ```
- **Payload:**
  ```json
  {
    "type": "agent-turn-complete",
    "thread-id": "session-id",
    "turn-id": "turn-id",
    "cwd": "/working/dir",
    "input-messages": ["user prompt"],
    "last-assistant-message": "response text"
  }
  ```

This is essentially equivalent to just a `stop` hook — no steering, no blocking, no return values.

### What's In Progress (Internal, Not Wired to Config)

The Codex team has merged internal infrastructure in Rust:
- **`AfterAgent`** event (PR #9691, v0.99.0) — the `notify` config uses this internally
- **`AfterToolUse`** event (PR #11335, v0.100.0) — explicitly marked "not wired up to config yet"
- **Hook error handling** (PR #11615) — enables hooks to fail/abort, prep for more hook types

### What Doesn't Exist Yet

There are **no equivalents** for the […]