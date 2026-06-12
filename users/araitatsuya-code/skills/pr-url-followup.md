---
name: pr-url-followup
description: "Trigger: user wants the agent to act on a specific GitHub PR or inline comment. User pastes the raw URL on line 1, then a short Japanese question or instruction on line 2."
---

This user never wraps GitHub URLs in markdown links or provides extended context. They drop the URL bare on its own line, then add a ≤10-word Japanese instruction on the next line. The agent is expected to fetch the PR/comment from the URL and act.

**Examples:**

> `https://github.com/araitatsuya-code/atena-print/pull/14#discussion_r2875523574`  
> `こちらも対応できる？`

> `https://github.com/araitatsuya-code/atena-print/pull/22`  
> `レビュー対応お願いします`

> `https://github.com/araitatsuya-code/atena-print/pull/15`  
> `レビュー対応できますか？`

**Structure:** raw URL + newline + short Japanese instruction (question or imperative).

**What this covers:**
- Responding to inline review comments on a specific PR
- Addressing all review comments on a PR
- Following up on a specific discussion thread

**How to reproduce this voice:** Just the URL and one line. Never "このPRを見てください" or any preamble.
