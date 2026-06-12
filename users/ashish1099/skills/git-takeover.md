---
name: git-takeover
description: Overrides the agent's git workflow with a direct command that also declares the current staging state — triggered when the agent finishes a task and is about to make staging decisions.
---

After the agent produces a task-completion summary, ashish1099 does not acknowledge the summary.
Instead they issue a short git command that simultaneously tells the agent what to do AND
corrects an assumption the agent was about to make about staging. The canonical form is:

> "commit this and its already in staged"

The conjunction "and its already in staged" (note: no apostrophe) preemptively blocks the agent
from running `git add` — ashish1099 has already staged the files themselves. This pattern
appeared in two separate sessions with identical wording, making it a reliable habit.

When the staging state is not in question, the message collapses to the minimum:

> "commit this"

The agent should interpret either form as: run `git commit` with appropriate message, do not
run `git add`, do not ask for confirmation.

**Example 1:**
> agent: "All tests pass. Here's a summary of the changes: **`pkg/gsync/openvox.go`** — …"
> user: "commit this and its already in staged"

**Example 2:**
> agent: "Done. Here's a summary of the changes: ### Where `global.yaml` is read from …"
> user: "commit this and its already in staged"
