---
name: plan-dump-kickoff
description: >-
  Trigger: kgcrom opens a "create new code" session. They paste a full Korean
  implementation plan they authored themselves, preceded by "Implement the
  following plan:" in English. The plan includes context (## Context), root
  cause (## 원인 분석), and step-by-step changes (## 수정 계획 or ## Changes)
  with file paths and code snippets. The agent should execute — not re-plan.
---

kgcrom does not delegate planning to the agent. They write the design spec first (often in Claude Code's plan mode), then open the implementation session by dumping the entire spec as the first message.

The spec is always in Korean, structured with `##` headers, markdown tables, and fenced code blocks. It ends with a `## 검증` (verification) section describing how to run the app and confirm the fix visually.

**Pattern**:
1. English trigger line: `"Implement the following plan:"`
2. Korean header: `# <제목>` (often the GitHub issue title)
3. Sections: `## Context`, `## 원인 분석`, `## 수정 계획` or `## Changes`
4. Each change: file path, before/after code, table of param changes
5. `## 검증`: `uv run cluefin-desk` + numbered visual checks

**Verbatim example (opening)**:
```
Implement the following plan:

# Fix: Stock Detail 차트 렌더링 깨짐 수정

## Context

종목 상세 화면의 가격 차트가 가로 검은 막대 아티팩트와 함께 깨져서 보임. 원인은 `plotext.build()`가 반환하는 **ANSI 이스케이프 코드**를 Textual의 `Static.update()`에 직접 전달하고 있기 때문.

## 수정 파일

- `apps/cluefin-desk/src/cluefin_desk/widgets/price_chart.py` — 유일하게 수정 필요한 파일

## 변경 사항

1. `from rich.text import Text` import 추가
2. `self.update(chart_str)` → `self.update(Text.from_ansi(chart_str))` 변경

## 검증

`uv run cluefin-desk` 실행 후 종목 선택하여 차트 탭에서 가격 차트가 정상 렌더링되는지 확인.
```

**Verbatim example (shorter/vague kickoff)**:
```
.github/PULL_REQUEST_TEMPLATE.md 만들어줘. 오픈소스 pull request template best practice 조시해서 해당 프로젝트에 맞게 수정해줘
```
