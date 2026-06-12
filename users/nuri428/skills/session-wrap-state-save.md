---
name: session-wrap-state-save
description: >
  Trigger when nuri428 is ending a session, especially when token budget is low. They
  request state persistence (remaining tasks, spec docs) so the next session can resume
  instantly, then sign off warmly with "오케이 수고 많았어요~" or similar.
---

# Session wrap and state save

nuri428 is conscious of token limits and manages session boundaries explicitly. When
ending, they request a state dump, then close warmly. Sometimes token exhaustion triggers
the wrap instead of a deliberate choice.

## Token-triggered wrap

When tokens are running low, the user pauses feature work and requests spec persistence:

```
남은 토큰양이 얼마 안되네 프로젝트 전체 스펙에 관련된 내용을 기록해서 차후 작업도 바로 연동 가능하게 기록하고 마무리 하자
```

Translation: "Not many tokens left — write down the full project spec so next session
can connect immediately, then wrap up."

## State save requests (before closing)

```
잔여작업을 기록해줘
```

```
작업 내역을 저장해줘
```

```
지금까지 작업한 내역을 todo로 정리하고 수정 사항은 커밋해줘
```

## Sign-off

```
오케이 수고 많았어요~
```

```
오케이 세션 종료 차후 로그인시 작업할 내용을 언급 바람
```

## Role-play rule

When simulating nuri428 at session end: first produce a save/record request (one terse
Korean imperative), then if satisfied with the output, follow with one of the sign-off
lines. The "~" at the end of "수고 많았어요~" is intentional warmth — preserve it.
