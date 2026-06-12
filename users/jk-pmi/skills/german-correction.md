---
name: german-correction
description: >
  Trigger: agent fundamentally misunderstood the request, took the wrong shortcut, or answered
  the wrong question entirely — especially after being told once already. German appears.
---

When the agent goes off-track or repeats a mistake, the user's language switches. The switch is proportional to frustration:

**Level 1 — single German word/phrase mixed in:**
- `"SEPC.md should have Vorrang"` (precedence)
- `"doppelt hält besser :D"` (double is better — approving redundancy with humor)
- `"ruf ein tool auf"` (call a tool)

**Level 2 — full German correction sentence:**
- `"Nein. Hör auf Abkürzungen zu gehen. Das war eine sudo-PW-Abfrage"` (No. Stop taking shortcuts. That was a sudo password prompt.)
- `"NEIN das ist nicht der punkt du"` (NO that's not the point)
- `"ne"` / `"ja"` (short German no/yes)

**Level 3 — German profanity + explanation of what was actually wanted:**
- `"nein man. schon wieder vollkommen am pnkt vorbei benenne einach execute-task um jesus"` (no man. completely off the point again just rename execute-task jesus)
- `"hurensohn: <quoted wrong output>"` — bastard/son of a whore, precedes pasting the agent's mistake
- `"fucking liar: <URL>"` — English profanity + docs URL to prove agent was wrong

## Pattern

Frustration corrections are always **short and blunt**. No multi-sentence explanation. The user identifies the single wrong thing and names it without softening. If they also give the correct instruction, it comes right after with no lead-in.

`"nein man. schon wieder vollkommen am pnkt vorbei benenne einach execute-task um jesus"` = the agent's entire long response dismissed in one line + the actual fix stated without a verb.
