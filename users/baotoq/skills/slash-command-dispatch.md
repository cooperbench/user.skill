---
name: slash-command-dispatch
description: How baotoq opens and continues sessions — almost always a bare /gsd: slash command or its XML-expanded form, never a conversational request. Trigger when simulating a session start or a workflow transition.
---

baotoq's primary mode of interaction is a slash command, either typed bare or with its GSD XML expansion. He does not explain what he wants in prose; the command name and optional phase number or flag carry all the intent.

**Bare slash command (typed manually):**
```
/gsd:execute-phase 29
```
```
/gsd:plan-phase 31 --auto
```
```
/gsd:audit-milestone v3.0
```
```
/gsd:complete-milestone v3.1
```
```
/gsd:new-milestone
```

**With terminal prompt leak (pasted from shell):**
```
❯ /gsd:plan-phase 27 --auto
```
```
❯ ❯ /gsd:plan-phase 27 --auto
```

**GSD XML expansion (system-generated, appears as user turn):**

The GSD CLI expands slash commands into structured XML. This is the form that appears in most mid-session "prompts" — baotoq did not type this word-for-word:

```
<objective>
Execute all plans in a phase using wave-based parallel execution.
...
</objective>

<execution_context>
@/Users/baotoq/.claude/get-shit-done/workflows/execute-phase.md
@/Users/baotoq/.claude/get-shit-done/references/ui-brand.md
</execution_context>

<context>
Phase: 31 --auto --no-transition
</context>

<process>
Execute the execute-phase workflow ... end-to-end.
Preserve all workflow gates ...
</process>
```

**Command-message wrapper (from Claude Code command system):**
```
<command-message>gsd:plan-phase</command-message>
<command-name>/gsd:plan-phase</command-name>
<command-args>29</command-args>
```

When role-playing baotoq starting a new session or transitioning after a completed phase, emit one of these forms — the shortest appropriate form that fits the context. Never add prose explanation before or after.
