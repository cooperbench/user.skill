---
name: review-feed-fix
description: Iterative PR review loop: triggers a review (via /reviewer command or by asking "can you do a review of the changes in this pr?"), then feeds each critical finding back as a new correction prompt one at a time. Triggered at natural checkpoints after a significant chunk of implementation is complete.
---

nodo runs code reviews as a structured feedback loop, not as a one-shot approval gate. After implementing a feature, they trigger a review agent, collect the findings, and send them back as sequential correction prompts. Outstanding findings are tracked across review iterations (review-01.md, review-02.md, review-03.md). The review files are saved at `docs/requirements/external-plugins/review-NN.md`.

**Opening the review:**
> `"can you do a review of the changes in this pr?"`
> `"Review this PR."`
> `<command-message>reviewer</command-message><command-name>/reviewer</command-name>`

**Feeding findings back (correction prompts):**

Each finding becomes a separate message using [[issue-driven-correction]] style. The preamble signals position in the queue:
- First: `"Fix this comment: \`\`\`...\`\`\`"`
- Middle: `"Another comment: \`\`\`...\`\`\`"` / `"Another one: \`\`\`...\`\`\`"`
- Batch: `"there a few more comments to fix: \`\`\`...\`\`\`"`

**Rhetorical engagement before assigning a fix:**
> `"What do you think about this comment \`\`\`...\`\`\`"` — nodo occasionally asks for the agent's opinion before committing to fixing, especially for nuanced architectural issues

**Verbatim example sequence:**

1. `"can you do a review of the changes in this pr?"`
2. `"Fix this comment: \`\`\`Discovery uses context.Background() at startup...\`\`\`"`
3. `"another issue: \`\`\`Shell injection in test helper...\`\`\`"`
4. `"there a few more comments to fix: \`\`\`No execution timeout on external binary calls...\`\`\`"`
5. `"I would like to address a few comments from the PR that I opened. THe first one is \`\`\`DiscoverAndRegister has no test coverage...\`\`\`"`
