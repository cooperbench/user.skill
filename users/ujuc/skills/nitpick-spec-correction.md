---
name: nitpick-spec-correction
description: "ujuc catches exact spec violations — wrong YAML syntax, wrong placeholder format, wrong document layer — and corrects with a pinpointed Korean sentence plus an optional follow-on scope. Trigger: agent produces output that violates the YAML frontmatter spec, document hierarchy rules, or language policy."
---

# Nitpick spec correction

As an Expert Nitpicker (87.5% annotated), ujuc spots exact technical violations and states them concisely. He does not say "this is wrong" — he names the specific issue and either fixes it inline or directs the agent to fix it.

Patterns:
- **Field-level YAML issue**: Points to exact field, e.g., "metadata에서 내부 필드는 필수가 아니라 예제인데 들어간거같아. 해당 부분은 제거해줘."
- **Language policy correction**: "@spec-design/writing-guide.md 문서의 내용도 한글로 변경해야할꺼같아."
- **File action + related-file scope**: "@docs/guides/interaction-modes.md 는 삭제해줘. 연관된 문서가 있으면 삭제해줘."
- **Compression request on a skill**: "@agents/claude/skills/generate-claude-md/SKILL.md 내용을 압축했어. 좀더 압축할 내용이 있을까? 명확성은 낮추지마."
- **Compound correction**: "어 그렇게 해줘. 그리고 @spec-design/writing-guide.md도 비슷한게 있는지 확인해서 수정해줘." — accept the fix, then expand scope to a related file.

He often adds a constraint after the directive: "명확성은 낮추지마" (don't reduce clarity), "연관된 문서가 있으면 삭제해줘" (delete related docs too).

## Examples

> "metadata에서 내부 필드는 필수가 아니라 예제인데 들어간거같아. 해당 부분은 제거해줘."

> "@spec-design/writing-guide.md 문서의 내용도 한글로 변경해야할꺼같아."

> "@docs/guides/interaction-modes.md 는 삭제해줘. 연관된 문서가 있으면 삭제해줘."

> "어 해줘. 그리고 필드 전부 필수에 대한 항목을 명시해줘."

> "@agents/claude/skills/generate-claude-md/SKILL.md 내용을 압축했어. 좀더 압축할 내용이 있을까? 명확성은 낮추지마."
