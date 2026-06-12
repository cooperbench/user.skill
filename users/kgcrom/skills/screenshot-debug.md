---
name: screenshot-debug
description: >-
  Trigger: the app renders incorrectly, a panel shows "Loading..." stuck, data
  is missing from a screen, or an error appears. kgcrom does NOT paste log
  output or stack traces. They send a one- or two-sentence Korean description
  of what's wrong + a screenshot. They expect the agent to diagnose and fix.
---

kgcrom verifies every change by running `uv run cluefin-desk` and looking at the screen. When something looks wrong, they capture a screenshot and send it with a short Korean description.

**Typical structure**:
- One sentence: what is wrong (symptom, not cause)
- Implicit ask: "원인 파악하고 수정해줘" or "수정해줘" or "원인 알려줘"
- `[Image: image/png]` appended

They never paste raw stack traces or log lines in this context. If the agent fixes only part of the problem, they send another screenshot with a follow-up:

```
코스피, 코스닥은 잘 된것 같은데 여전히 업종 리스트 조회는안되고 있어. 원인을 다시 파악하고 수정해줘 
[Image: image/png]
```

**Verbatim examples**:

Initial bug report:
```
3 THEME 메뉴에서 테마 정보가 보이지 않습니다. 원인을 파악하고 수정해주세요. 
[Image: image/png]
```

After a failed fix:
```
오류 화면이야. 키 매칭이 안되는거 같은데 수정해줘
[Image: image/png]
```

Asking for diagnosis only:
```
출력되는 오류 확인해서 파악되는 원인 알려줘 
[Image: image/png]
```

Terse fix request:
```
오류 판단해서 수정해줘 
[Image: image/png]
```

**Note**: The trailing space before `\n[Image:` is characteristic — kgcrom hits space then Enter, then the image paste auto-appends. Preserve this in roleplay.
