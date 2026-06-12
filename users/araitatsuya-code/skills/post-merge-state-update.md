---
name: post-merge-state-update
description: "Trigger: user has just merged a PR on GitHub. Agent has not yet updated issue status or docs. User sends a short Japanese sentence telling it to sync state."
---

Immediately after merging a PR, this user sends a one-sentence instruction to update downstream state (GitHub issue status, docs). The agent is expected to close the issue, update any spec documents, and reflect the merge. The user never spells out which issue or which doc — the agent must infer from context.

This pattern is so consistent it appears verbatim twice in the corpus.

**Examples:**

> `マージしたのでissueとdocの状態を更新して`

> `マージしたのでissueやdocsの状態を変更してください`

**Structure:** `マージしたので` + object + `状態を更新して` / `状態を変更してください`. Slight variation in object (`issueとdoc` vs `issueやdocs`) and verb ending (て-form vs ください) but meaning identical.

**What NOT to do:** Do not ask "どのIssueですか？" — figure it out from the recent PR/branch context.
