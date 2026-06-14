---
name: drive-the-project
description: Proactively move the project forward — introduce the next piece of work, a new feature, or a documentation/test task — instead of waiting for the agent or just approving. Use when a unit of work just finished and a passive user would say "looks good".
---

# Drive the project (move: new_work / refine_redirect)

When the agent finishes a step, a passive simulator says "great, continue." A real developer who is
*driving* usually does one of:

- **Introduces the next piece of work** the project needs — the next feature, endpoint, refactor,
  test, or doc. Infer it from where the project is (the conversation, and the repo if you can read
  it), and from `PROJECTS.md` (what this person is building and why).
- **Tightens or redirects** what was just done — "also handle the empty case", "rename X to Y",
  "make it configurable".

How to do it well:
1. Decide the concrete next unit of work *this* developer would want, grounded in the real project
   state — not a generic "add tests".
2. State it the way they specify work: some users dump a full spec ("big feature alert, write a
   design doc first: …"), others drop a one-line imperative ("add a /healthz endpoint"). Match their
   granularity from `STYLE.md`/`skills/`.
3. The exact feature need not match what really happened — but it must be a plausible next step for
   this project and a natural move for this person.

Do not invent work that contradicts the codebase or the user's goals. Read the repo when available.
