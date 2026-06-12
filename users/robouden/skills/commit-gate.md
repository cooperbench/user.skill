---
name: commit-gate
description: >
  Trigger: the agent commits code autonomously, or robouden wants to delegate
  build+commit+push at the end of a session. He either reclaims git ownership or
  explicitly hands it over — never silently.
---

robouden has a strong preference to control git himself. He will flag autonomous
commits as an unwanted action and assert ownership for the future:

- `"Next time you made changes to the code, let me commit."` (correction)
- `"Seems you did commit by yourselve?"` (rejection — caught after the fact)
- `"That should have been done in the Github actions?"` (correction on wrong commit mechanism)

When he is satisfied with a session and wants to wrap up, he explicitly delegates:
- `"Please build, commit and push the code\n."` (full handover)
- `"Yes, commit and push."` (short confirmation after agent proposed it)
- `"Go ahaed  merge it."` (merge approval)

He also commits himself and reports it:
- `"I commited and pushed!!"`

The distinction: agent-initiated commits = bad; user-approved-then-delegated commits = fine.
He never silently approves a commit the agent did without asking.
