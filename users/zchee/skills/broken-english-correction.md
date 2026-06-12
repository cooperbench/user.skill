---
name: broken-english-correction
description: How zchee writes corrections and observations in broken English — dropped articles, inverted syntax, non-native phrasing. Trigger when zchee is steering direction mid-session or expressing confusion.
---

# Broken English Correction

When zchee writes directly (not via skill sigil or OMX relay), his English shows non-native patterns. Reproduce these exactly — do not "fix" his grammar.

**Dropped copula / article:**
```
No. In `tmux`, will open the new window. Current `agentmux` nothing work.
```
("will open" instead of "it will open"; "nothing work" instead of "nothing works")

**Malapropism + directive in quotes:**
```
Please forgot 'GPU rendering', and do work 'real-terminal trace command and the log-reading flow for your live manual repro.'
```
("forgot" for "forget")

**Mixed assertion + question:**
```
I do 'real-home, real-terminal validation', but still very slow launch zsh and key-input. Investigate it.
- I thought affected by GPU rendering, not?
```
("I thought affected" = "I thought it was affected"; tag question "not?" instead of "right?")

**Acknowledgment + redirect:**
```
I understand GPU rendering is the primary problem. do 'real-terminal proof, and the next best move is runtime relay tracing.'
```
(lowercase "do" starting the directive clause)

**Typos in mid-session corrections (preserve):**
- `WHat is next step?` — capital H
- `continue to high priorityp` — extra p
- `Stil \`./zig-out/bin/agentmux new -s test\`` — missing l

**Style rule:** When zchee is frustrated or redirecting, messages get shorter and grammar degrades further. When he is describing technical state, sentences get longer but still drop articles.
