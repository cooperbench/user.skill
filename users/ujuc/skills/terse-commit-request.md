---
name: terse-commit-request
description: "ujuc requests commits with minimal Korean words, sometimes mid-sentence as a takeover. Trigger: after any discrete set of file changes, or when the agent stops mid-session."
---

# Terse commit request

ujuc commits frequently and asks for commits concisely. He never describes what to commit in the commit message himself — the agent must figure out the scope from git status/diff and write Korean Conventional Commits.

Commit request forms (in order of frequency):
- `"커밋해줘."` — most common; commit everything staged
- `"수정된것들을 전부 커밋해줘."` — commit all modifications
- `"지금까지 수정한 내용에 대해서 정리해서 커밋해줘."` — summarize changes into a commit
- `"문서에 대해서 작업한 내용들을 커밋해줘."` — commit the document work
- `"변경사항들을 커밋해줘."` — commit the changes

Occasionally appears as a **takeover mid-session**: agent is outputting something and he interrupts with `"커밋해줘."` expecting the agent to stop and commit.

## Examples

> "커밋해줘."

> "수정된것들을 전부 커밋해줘."

> "지금까지 수정한 내용에 대해서 정리해서 커밋해줘."

> "문서에 대해서 작업한 내용들을 커밋해줘."

> "변경사항들을 커밋해줘."
