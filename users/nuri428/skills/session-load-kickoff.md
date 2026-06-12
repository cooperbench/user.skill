---
name: session-load-kickoff
description: >
  Trigger at the very start of a new session. nuri428 always opens by asking the agent to
  load state from project files (claude.md, tasks.md, project.md) rather than explaining
  context themselves. They expect the agent to reconstruct the full project picture
  from those files.
---

# Session load kickoff

nuri428 opens sessions by asking the agent to load context from disk. They never
re-explain the project, the stack, or prior work — that's all in the files. The opening
message is short (3–8 words) and either Korean or English.

## Variants

**Korean (most common)**:
```
claude.md를 읽어서 이전 세션에서 중단한 내용을 로딩해줘
```

**Mixed (terse)**:
```
load todo znd tasks and claude md files
```

**Status check (English one-liner)**:
```
entire status
```

**Spec file load**:
```
tasks.md, project.md 같은 md 파일을 읽어서 프로젝트 스펙을 조회해봐
```

**Feature doc load**:
```
기능정의서 문서가 있을거야 그걸 로딩해봐
```

## Role-play rule

When simulating nuri428 opening a session, produce one of these patterns (or a close
variant). Do NOT provide context. Do NOT explain what you want done — the agent is
expected to figure it out from the files. Typos like "znd" are authentic; preserve them.
