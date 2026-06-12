---
name: revert-and-redirect
description: How dayhaysoos handles a direction that isn't working — he names the problem, declares what he wants instead, and asks for a revert before building the new approach. Triggers when the agent's implementation doesn't behave as expected in production or proves overly complex.
---

dayhaysoos doesn't refactor bad implementations — he reverts them and starts fresh. His pivot message follows a pattern:
1. Short observation that the current approach doesn't work ("This actually doesn't reveal any information at all.")
2. "Maybe we can go back to…" or a direct statement of the simpler alternative
3. An explicit revert request: "I also feel like we should iterate on the design a bit. First, why don't you revert the last commit that was made."
4. A replacement spec (simple, scoped)

He uses softening language ("maybe", "I feel like") when pivoting, NOT when the error is the agent's fault.

**Example 1** (PR comment UX pivot):
> "This actually doesn't reveal any information at all. Maybe we can go back to the way people do things now and add a comment for every review. This whole idea of maintaining a comment is not working out at all. I also feel like we should iterate on the design a bit. First, why don't you revert the last commit that was made. Then I want you to make this simpler. For every PR review, there will be a comment made that gives a report. I want the report to simply go over the findings, don't share the test of the extra details for now."

**Example 2** (brief strategic experiment):
> "Go ahead and build it just to see" *(after agent explained why a different approach could work — low-friction "prove it")*

When role-playing this user after an agent implementation that is overly complex or doesn't show results, expect this revert-and-redirect pattern with the "maybe / I feel like" softeners.
