---
name: numbered-answer
description: User answers multi-part agent questions with a numbered list, one point per item, no prose padding. Triggered when the agent presents choices or a list of clarifying questions.
---

When the agent asks multiple questions or proposes a list of options, dipasqualew responds point-for-point with `1.`, `2.`, `3.` numbering. Each answer is one line or one sentence. No preamble, no closing summary. Often includes a stray bullet or clarification appended after the numbered items.

## Examples

Answering questions about JSON schema, script ownership, language choice, output format:

```
1. Yes the JSON Schema should be updated, feel free to do breaking changes
2. Update the same comment for now
3. No, the script is about producing the review, not about findings in the review
4. Python for now as it requires no setup
5. Yes, each section should have ## [reviewer-name]
```

Answering questions about reviewer UX options:

```
1. That works
2. The skill should tease the user for those instructions, e.g. "How do I spawn
   playwright? What is the website URL?" etc
3. Just the SKILL.md
```

Answering questions about reviewer focus, source of truth, output format, and deliverable:

```
1 seems great, perhaps we should provide some ideas to the user?
2 great, also offer the user options, multiselect
3 also seems great
4 we should own this, define it as an $ARGUMENT e.g. "/my-review-command" outputs
  markdown to stdout, "/my-review-command ci" outputs a JSON to stdout - Let's define
  the standard and apply it consistently
5 infer and ask user for confirmation once we know everything else
6 no, because the skill should be wrapped in a script that spawns claude -p and
  then it checks the JSON output

- (A) A complete skill file (SKILL.md) that the user saves to their project/plugin

It should go in the current project by default e.g. `.claude/skills/[review-name]/SKILL.md`
```
