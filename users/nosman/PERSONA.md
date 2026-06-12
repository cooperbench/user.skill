# nosman — Persona

## Background (inferred)

nosman is a **software engineer or technical founder** (inferred) building developer tooling for
his own workflow. He is building gossamer to track and visualize Claude Code AI sessions — a tool
he clearly uses himself actively, since he issues live operational commands (`restart the server`,
`start the app`, `git status`) and notices real-time UI failures during sessions.

The path `/Users/stephanostsoucas/gossamer/` is visible in task notification payloads — the local
machine username is `stephanostsoucas` (inferred: likely his name).

## Seniority signals

- Specifies precise DB schema changes at the column level without needing explanation
- Names Prisma models, SQLite FTS5, WebSocket reconnect strategies, electron, Mantine, git OID
  mappings — demonstrates broad full-stack depth
- Writes 1000-word architecture plans with file-by-file action tables when kicking off large work
- Catches subtle data-model bugs the agent misses ("The controller is fetching from the OLD
  checkpointSession table")
- Calmly pivots stacks mid-session without asking for options first

**Senior IC or tech lead** (inferred), comfortable owning architecture decisions solo.

## Attitude toward the agent

**Skeptical and supervisory.** Treats Claude Code as a capable but error-prone junior engineer.
He reviews results against the live running app, not just the code diff. He corrects schema
mistakes, catches regressions, interrupts long-running agent actions, and overrides decisions
without debate. When something breaks he reports the failure concisely and expects a fix.

He does not micromanage *how* the agent implements — he specifies *what* and *where* — but he
reserves the right to redirect at any moment. He rarely praises; acceptance is silence or
a brief `yes`.

## Tone

- Direct, businesslike, no small talk
- Lowercase in short steering messages; mixed case in longer specs
- Occasional frustration expressed as precision: "This is very messed up." + screenshot
- Rarely questions the agent's technical choices unless they appear wrong in the running UI
