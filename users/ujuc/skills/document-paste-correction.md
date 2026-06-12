---
name: document-paste-correction
description: "When the agent's output violates a principle or misses content, ujuc's correction is to paste the raw source document — not an explanation. Trigger: agent produces something that contradicts an existing guideline or misses required content."
---

# Document-paste correction

ujuc's most distinctive correction behavior: instead of explaining what the agent did wrong, he pastes the actual document that should have guided the agent's behavior. The pasted content is the correction signal.

This manifests two ways:

**1. Principle injection** — agent violated a design philosophy, so he pastes the philosophy document:
- After agent produces a verbose insight summary: pastes "LLM 컨텍스트 원칙" with bullet points on why style rules don't belong in CLAUDE.md
- After agent produces wrong CLAUDE.md content: pastes the 4-step validation checklist

**2. Pipeline continuation** — agent completed one document migration, he pastes the next document to migrate (no "great, now do the next one" — just the raw document):
- After monitoring.md migration completes: immediately pastes output-formats.md source XML content
- After interaction-modes.md is deleted: immediately pastes the next document body

The agent must recognize: **a large XML or markdown document pasted after a completion message means "process this next using the same transformation"**.

## Examples

**Principle injection after wrong philosophy:**
> "## LLM 컨텍스트 원칙\n\n- LLM은 인컨텍스트 학습자다. 기존 코드 패턴을 검색하면 스타일을 자연스럽게 따라가므로, 스타일 규칙을 CLAUDE.md에 포함할 필요가 없다.\n- Claude Code 시스템 프롬프트가 이미 ~50개 지시사항을 포함하며, 보편적이지 않은 내용이 많을수록 전체가 무시될 확률이 높아진다. [...]"

**Pipeline continuation (next document, no preamble):**
> "# Output Format Standards\n<meta>\nDocument: output-formats.md\nRole: Response Format Guide\n[...XML document body...]"
