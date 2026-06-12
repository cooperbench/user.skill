---
name: mid-session-pivot
description: evisdren redirects the agent to a completely different issue or scopes the current task down, often mid-execution. Trigger when evisdren wants to change topic, scope, or approach without finishing the current thread.
---

# Skill: mid-session-pivot

evisdren changes direction often (33% Mind Changer annotation). They do not wait for the agent to finish or wrap up the current task — they interrupt and redirect. The pivot message is terse and direct, often starting with "no not yet", "let's start with", or "okay now let's do". They may also interrupt with a completely new issue introduced as "somebody on github posted that..." or similar external trigger.

## Characteristics

- Starts with a direction signal: "no not yet.", "let's start with", "okay", "actually"
- Does not apologize for changing direction
- May scope a numbered list: "let's start with implementing suggestions 1-4 first", "okay now let's do 6,7,8,10"
- May pivot to a completely different issue with a brief framing sentence
- Typos present when improvised: "no not yet. i want to focus on another issue. somebody on github posted taht..."
- Sometimes accompanied by `[Request interrupted by user for tool use]` — they literally stop the agent mid-run

## Verbatim Examples

**Example 1 (interrupting benchmark work to fix a user bug report):**
> "no not yet. i want to focus on another issue. somebody on github posted taht they were trying to use homebrew to install  our CLI:\n\nI installed entire using brew, but when I try running entire enable on a repo I see this dialog and it fails with zsh: killed     entire enable.\n\n\nand got a malware detection issue. \n\nevaluate the claim and what could have caused this"

**Example 2 (scoping an agent-suggested list):**
> "let's start with implementing suggestions 1-4 first"

**Example 3 (continuing the scope after first batch):**
> "okay now let's do 6,7,8,10"

**Example 4 (terse after interrupting):**
> "Continue from where you left off."
