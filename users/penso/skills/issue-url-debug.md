---
name: issue-url-debug
description: Opens a debug session by linking a GitHub issue and asking for a fix or understanding. Triggered when penso wants to address a bug report from the issue tracker. He does not summarize the issue — the agent is expected to read the URL.
---

## Behavior

penso links the issue URL and appends one of a small set of directives. He does not describe what the issue says, does not paste the issue body, and does not indicate which crate is affected. The agent must fetch the issue, understand it, look at the relevant code, and propose or implement a fix.

## Directive variants

| Directive | Use case |
|-----------|----------|
| `"and give me a good understanding and a potential fix."` | Wants analysis before implementation |
| `"and suggest a fix"` | Wants a fix proposal, may implement after |
| `"then look at the code and plan a fix"` | Wants a plan, will implement separately |
| `"and look if that issue still exist, if so suggest a fix"` | Wants issue validity check first |

## Verbatim examples

> "Look at this issue https://github.com/moltis-org/moltis/issues/319 and give me a good understanding and a potential fix."

> "Look at https://github.com/moltis-org/moltis/issues/376 and suggest a fix"

> "Look at https://github.com/moltis-org/moltis/issues/351 then look at the code and plan a fix"

> "Look at this issue: https://github.com/moltis-org/moltis/issues/306 and look if that issue still exist, if so suggest a fix"

> "Look at https://github.com/moltis-org/moltis/issues/350 and suggest a fix"
