---
name: unknown-skill-error-paste
description: >
  Trigger when a Claude Code plugin slash command fails. nuri428 pastes "Unknown skill: X"
  verbatim as their entire next message — no commentary, no explanation. This is both a
  failure report and an implicit retry signal.
---

# Unknown skill error paste

When a slash command fails (plugin not found, version mismatch, or Claude Code not
recognising the skill), nuri428's only response is to paste the error exactly:

```
Unknown skill: pdca
```

or

```
Unknown skill: rc
```

or

```
Unknown skill: pda
```

(Note: "pda" and "paca" are typos of "pdca" — user copies the error verbatim, not the
intended command.)

## What it signals

- The user expected the agent to handle this command natively
- They are telling the agent the previous attempt failed — not asking what happened
- They want the agent to either install the plugin, find an alternative, or re-invoke
  differently — they do NOT want a diagnosis unless something is visibly broken

## Verbatim examples

```
Unknown skill: pdca
```

```
Unknown skill: pda
```

```
Unknown skill: rc
```

```
Unknown skill: remote-control
```

```
Unknown skill: paca
```

## Role-play rule

When simulating nuri428 after a plugin command fails, output ONLY the "Unknown skill: X"
line with no surrounding text. Do not explain or prefix.
