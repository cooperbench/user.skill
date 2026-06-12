---
name: tool-interrupt-takeover
description: How alishakawaguchi interrupts mid-execution when they've already decided the next step — they cancel the current tool call and immediately issue the next command. Trigger when the agent is mid-explanation or mid-execution and the user has seen enough.
---

# tool-interrupt-takeover

alishakawaguchi frequently interrupts agent tool use before it completes. The interrupt appears as `[Request interrupted by user for tool use]` or `[Request interrupted by user]` in the transcript. Immediately following the interrupt, they issue the next directive — usually a git operation, a slash command, or a terse correction.

This is a takeover pattern: they don't wait for the agent to finish, and they don't acknowledge what was interrupted. The next message is simply the next step.

## Behavior pattern

- Interrupt mid-tool-use with no explanation
- Follow immediately with the intended action
- Most common post-interrupt actions: "commit and push", `/commit-commands:commit`, "yes", numbered option

## Examples

**Takeover to commit:**
```
[Request interrupted by user for tool use]
```
followed by:
```
<command-message>commit-commands:commit</command-message>
<command-name>/commit-commands:commit</command-name>
```

**Takeover with immediate confirmation:**
```
[Request interrupted by user for tool use]
```
followed by:
```
yes
```

**Takeover to redirect (agent was heading wrong direction):**
```
[Request interrupted by user]
```
followed by:
```
why do I have to load it like this? why can't it be auto loaded? claude --plugin-dir .claude/plugins/agent-integration/
```

## When this triggers (inferred)

- Agent is writing a long explanation the user already understands
- Agent is executing a tool (e.g., Read, Bash) and the user has decided they want to go a different direction
- Agent is about to commit/push but the user wants to use the slash command instead
- Agent's approach was rejected before the tool call even returned

## What they do NOT do

- Do not write "never mind" or "stop" — they use the interrupt UI feature
- Do not explain why they interrupted
- Do not re-state context after interrupting — next message is purely forward-looking
