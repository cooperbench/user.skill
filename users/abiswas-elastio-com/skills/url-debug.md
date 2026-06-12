---
name: url-debug
description: >
  Trigger: user is reporting a bug or unexpected behavior in the live app.
  They always include the live URL and often paste raw console errors or screenshots.
---

# URL-first debugging

When reporting bugs, this user leads with the live URL and expects the agent to fetch context from it. Abstract descriptions are rare — they point at production or staging directly.

Characteristics:
- URL always comes first or early: `https://taskai.cc/app/projects/1/tasks/19`
- May paste browser console errors verbatim (long stack traces with JS bundle hashes)
- May attach screenshots (`[Image: image/png]`) for visual bugs
- Minimal commentary — the URL + error is the full report
- Expects the agent to cross-reference what the URL shows with the code

**Examples:**
> "still issues with swim lanes and status, some of these are done but in swim lane to do check task and check screenshot in task description\n\nhttps://taskai.cc/app/projects/1/tasks/19"

> "why is this still running? https://github.com/anchoo2kewl/SprintSpark/actions/runs/22001641454"

> "https://staging.taskai.cc/app/projects/1 failed to fetch tasks Failed to load resource: the server responded with a status of 500 ()Understand this error\nindex-Xu_1xh6c.js:100 [useLocalTasks] Server fetch error: Error: failed to fetch tasks\n    at jS.request (index-Xu_1xh6c.js:67:3819)\n..."

> "i cannot login anymore invalid email or password\n\nhttps://staging.taskai.cc/login did we destroy the db again?"

> "you broke something https://staging.taskai.cc/login Unexpected token '<', \"<html> <h\"... is not valid JSON\n\n please don't break things, what are tests for then?"

When the bug is a UI positioning issue, they paste screenshots without explanation: the image is the bug report.
