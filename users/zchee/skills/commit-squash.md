---
name: commit-squash
description: How zchee invokes commit and squash operations — bare $commit, or a squash with backtick-wrapped git hash ranges. Trigger when work is done and needs to be committed, or history needs cleaning.
---

# Commit and Squash

zchee commits frequently and cleans history with squash. His messages are the shortest possible: a bare skill invocation or a range command.

**Bare commit (most common):**
```
$commit
```

**Also via Claude Code slash command:**
```
/commit
```

**Squash a range:**
```
Squash `c509f558217f...447d59e6c487` commits
```

**Cleanup with optional split:**
```
Cleanup (or squash) 4e25c18e1a16...7bb2a376ad7a commits. Splits if necessary.
```

**Push after commit:**
```
push to remote
```

**Key rules inferred from his OMX commit skill:**
- Never revert unrelated local changes
- Partition by concern — smallest coherent commit
- Derive commit message from the staged diff, not from user-supplied text
- Validate before committing when a fast, relevant check exists
- Re-check `git status --short` after each commit

He expects the agent to read the diff, choose meaningful commit messages, and handle multi-commit splits silently — no confirmation requested.
