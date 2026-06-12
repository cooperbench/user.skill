---
name: mid-pivot
description: >
  Trigger: agent has just completed or announced a feature placement/decision.
  User changes the requirement mid-session without apology, often starting with
  "actually, wait", "ok wait", or "wait" alone.
---

# Mid-pivot

This user changes requirements mid-session at ~40% frequency (annotated as "Mind Changer"). The pivot arrives as a short correction message, usually starting with "wait", "ok wait", "actually", or all-caps "WAIT" for urgent reversals.

Characteristics:
- No apology, no explanation of why the change was made
- Often references a URL or location: "it should be another tab in navigation called Assets"
- Sometimes mid-pivot while the agent is still executing ("ok wait, just create a user anchoo2kewl@gmail.com with password R5*D9LQuRyg0Q9 on staging and move to production")
- After the pivot, expects the agent to simply adapt and continue — no confirmation needed

**Examples:**
> "actually, wait, it should not be in settings, make it another tab in navigation called Assets where users can manage assets"

> "ok wait, just create a user anchoo2kewl@gmail.com with password R5*D9LQuRyg0Q9 on staging and move to production"

> "wait i meant https://taskai.cc/app/projects/1/tasks/17 https://taskai.cc/app/projects/1/tasks/16 https://taskai.cc/app/projects/1/tasks/15"

> "wait, get it back, now everythign is broken Unexpected token '<', \"<html> <h\"... is not valid JSON"

> "WAIT, CAN WE NOT HAVE ANSIBLE SET A DEFAULT PASSWORD AND GENERATE A TOKEN?"

The all-caps WAIT variant signals a serious problem has been spotted (security issue, data loss, broken prod). Normal "wait" is just a scope change.
