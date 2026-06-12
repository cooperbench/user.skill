---
name: spec-dump-kickoff
description: "Trigger: starting a new implementation session or a major new feature; user pastes a complete numbered spec document (400–754 words) as the opening prompt."
---

When kicking off a new feature or implementation phase, junjie does not describe what he wants conversationally — he pastes a complete, structured spec document. These specs include: context section, architecture decisions, commit-by-commit breakdown, specific file paths, exact function signatures, and even JSX layout diagrams.

The spec is written in a mixture of Chinese and English, uses markdown headers, code blocks, and tables. It reads like a PRD + technical design doc fused together. He has already done the design thinking before opening the session.

**Structure of a typical spec dump**:
```
Implement the following plan: # Plan: [Title]
## Context
[paragraph in Chinese or English]
## Architecture / Implementation ([N] commits)
### Commit 1: [layer] — [feature]
**File: `path/to/file.ts`** (new/edit)
[bullet-point implementation details with code snippets]
```

**Key signals**:
- Opens with "Implement the following plan:" or similar imperative
- References numbered specs: "Spec 002", "Spec 003", `003-smart-hire`
- Specifies exact file paths, not just component names
- Includes verification steps ("验证 1. ... 2. ...")
- May reference `@file/path` notation for context

This behavior alternates with ultra-terse steering — the bimodal signature of this user.
