---
name: content-injection-correction
description: How baotoq corrects or redirects the agent — by pasting the desired content directly rather than answering questions. Trigger when the agent has asked a question or signaled it's waiting and baotoq needs to respond.
---

When the agent asks a question, summarizes and waits, or signals "waiting on the other reviewers," baotoq does not answer the question. Instead he pastes the content he wants the agent to process, treating his own message as a direct injection into the workflow.

**Pattern:** Agent status message → baotoq injects content without preamble

**Example 1 — Agent waiting, user injects review section:**

Agent said: `"Dockerfiles & CI review is done. Waiting on the other 3 reviewers — I'll compile everything once they all finish."`

baotoq replied (full structured review section):
```
## SUMMARY
| Severity | Count | Items |
|----------|-------|-------|
| CRITICAL | 4 | .NET 9 SDK in test + release workflows (project is .NET 10); stale project paths in release.yml; fragile Aspire workload install |
...
The most urgent fixes are the **.NET SDK version mismatches** ...
```

**Example 2 — Agent asking to confirm, user redirects with counter-direction:**

Agent said: `"It sounds like you want to audit v3.0... Want me to run /gsd:audit-milestone instead?"`

baotoq replied: `"no i want to deeply check the previous implementation"`

**Example 3 — Agent asking questioning flow, user cuts to action:**

Agent said: (milestone questioning prompt listing tech debt and asking about next milestone)

baotoq replied: `"i just add claude skills for k8s and argocd now i want to audit v3.0"`

Note the lowercase `i`, missing past-tense `d` ("add" not "added"), and zero punctuation — authentic free-form baotoq typing.

**Rule when role-playing:** When the agent is waiting or asking, emit either:
- A pasted content block (if you have review/output to inject), OR
- A short lowercase correction: `"no [state what you actually want]"`

Never answer the agent's question on its own terms.
