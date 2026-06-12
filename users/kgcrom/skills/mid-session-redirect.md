---
name: mid-session-redirect
description: >-
  Trigger: the agent finishes a task but kgcrom sees something missing, wrong,
  or wants to pivot. They send a short Korean sentence (10–30 words) that names
  the specific wrong element and states what it should do instead. No re-explanation
  of the original plan. Sometimes self-corrects immediately after their own prior
  message.
---

When the agent completes work and kgcrom notices a gap or error, they redirect with a terse Korean correction — never re-pasting the spec, never explaining context the agent should already have. They point at the specific element and describe the desired behavior in one sentence.

**Patterns**:
- Specifying a missed behavior: `"switch_screen 했을 때 선택된 메뉴는 하이라이트 되서 지금 어떤 화면인지 보여줘."`
- Clarifying a visual behavior with screenshot: `"rank 화면에서 메뉴 선택했을 때 detail이 활성화 되는데 사실 두번째 사진에서 종목 detail이 활성화되고 상세보기가 가능해야되는데 확인해줘"`
- Language correction (self-redirect): `"아니다 미안. 영어로적어줘"` — immediately after their own previous message asked for Korean
- Scope correction with file table: sends a markdown table of `| 작업 | 파일 경로 |` rows to tell the agent what was missed

**Verbatim examples**:

After agent completes NavBar fix:
```
switch_screen 했을 때 선택된 메뉴는 하이라이트 되서 지금 어떤 화면인지 보여줘.
```

After agent commits and user changes mind:
```
해당 프로젝트의 description을 한글로 적어줘
```
(immediately followed by)
```
아니다 미안. 영어로적어줘
```

After agent misses eval file:
```
## 수정 대상 파일 요약

| 작업 | 파일 경로 |
|------|----------|
| 신규 | `.github/ISSUE_TEMPLATE/config.yml` |
| 신규 | `skills/create-issue/SKILL.md` |
| 신규 | `evals/skills/create-issue.eval.yaml` |
| 수정 | `evals/manifest.json` |
```

**Key**: kgcrom never says "you missed X" or "please also add Y". They just state what should exist or happen, implying the agent knows what to do.
