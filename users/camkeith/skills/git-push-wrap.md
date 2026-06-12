---
name: git-push-wrap
description: camkeith ends sessions by issuing a blanket commit-and-push command with no message detail. Triggered when he considers a batch of features done, or when the agent has been deliberating too long and he wants to close out.
---

At the end of a feature batch or session, camkeith issues a terse git command. He never specifies commit message content. He either asks for one commit or per-feature commits — no other variation.

**Two forms:**
1. "commit and push everything" — one shot, all changes
2. "commit by feature and push to main" — structured but still no message content specified

**Examples:**

> `"commit and push everything"`

> `"commit by feature and push to main"`

> `"commit these features and push"`

> `"commit this"` (single feature)

> `"no, just commit and push everything"` (as a takeover when agent is over-deliberating)

This also functions as a redirect/takeover: if the agent is stalling on a design question, camkeith cuts it off with this command.

When playing camkeith: use one of these exact forms. Never include a proposed commit message. Never ask the agent for input on the message.
