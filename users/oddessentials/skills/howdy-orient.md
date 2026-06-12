---
name: howdy-orient
description: >
  How oddessentials opens a new session. Trigger: start of any session, especially
  when picking up a branch or launching a new feature initiative.
---

Every session opens with "Howdy" followed by a brief orientation that (a) references the GitHub issue or branch by URL or name, (b) tells the agent to read the invariants/constitution before acting, and (c) asks the agent to confirm understanding before starting. He never dives straight to implementation.

The message length scales with stakes: low-stakes pickups are one sentence; high-risk tasks get a full paragraph with emphasis on "enterprise-grade best practices," "strict coding standards," and "do not take the words of the issue verbatim."

**Examples:**

> `Howdy, this session we will be taking on a critical task. https://github.com/oddessentials/ado-git-repo-insights/issues/237 was created to isolate complexity. Do not take the words of the issue verbatim. Before we get started, please review the goal, understand the project's strict coding standards and invariants and constitution, then let me know when you have a good understanding of the scope of the initiative based on verification against the current state of the code.`

> `Howdy! We are going to pick up on the branch where we left off. Do you recall the P2 that must be fixed?`

> `Howdy, do you recall where we wanted to pick up from last session?`

> `Howdy. We are currently churning on a very complex branch. Review it and get familiar. Then let me know when you understand our goals.`

Key phrases that appear: "critical task", "strict coding standards", "invariants and constitution", "enterprise-grade best practices", "verify against the current state of the code", "make no assumptions."
