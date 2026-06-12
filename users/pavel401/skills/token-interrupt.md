---
name: token-interrupt
description: How Pavel401 stops the agent from over-consuming context — interrupts tool calls mid-execution and explicitly tells the agent to stop reading when the token budget is threatened.
---

# token-interrupt

Pavel401 monitors tool calls in real time. When the agent starts reading files it doesn't need or runs sub-agents that burn tokens unnecessarily, he interrupts immediately — either via `[Request interrupted by user for tool use]` (a session-level interrupt) or by sending an explicit message telling the agent to work from existing context.

After interrupting, he expects the agent to continue from what it already knows — not to restart or ask for clarification.

## Triggers

- Agent is about to read a file it already has context for
- Sub-agent is spawning more tool calls than expected
- Agent accumulated too many tokens and is heading toward context overflow
- Agent uses an expensive orchestration pattern (multi-agent when 2-agent would do)

## Examples

**Example 1** — mid-session token warning:
```
No need to read the code write high level what you will change , you have already have  43.1k tokens                                     
   │  ⎿  Done                                       
   └─ Explore agent schemas and GitHub client context · 17 tool uses · 39.4k tokens    context don't fetch more else I will run out of tokens
```

**Example 2** — after burning money on a runaway orchestrator:
```
Ok Bro , just burned so much money for no reason ,from next time always warn me where things can go wrong . please put this in your caludemd , time to time update it as well . Should the claude.md be part of a oublic repo ?
```

**Example 3** — silent interrupt (shows in transcript):
```
[Request interrupted by user for tool use]
```

**Example 4** — redirect after an out-of-scope correction:
```
I meant how will we fix the Code review agent [pastes agent's analysis back] 
```
(tells agent: your analysis was right, now tell me the fix — don't re-read anything)
