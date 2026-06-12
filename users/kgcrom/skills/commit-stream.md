---
name: commit-stream
description: >-
  Trigger: kgcrom is satisfied with a change (or just wants to move forward).
  They send a /commit slash command, often followed immediately by the commit
  skill spec injected by the harness. This is the most frequent action in the
  dataset (51% of all intents are "git"). After committing, they may reset or
  amend if the message is wrong.
---

Git commits are kgcrom's pace-setter. They commit after every meaningful unit of work, using a custom `/commit` skill that enforces a strict format: English type prefix + Korean summary ≤50 chars, optional Korean body at 72-char wrap.

**Commit format (from their skill)**:
```
<type>: <short summary in Korean>

<optional body in Korean>
```
- Type in English: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`
- Summary and body in Korean
- Concise verb forms: "추가", "수정", "삭제" — NOT "추가하도록 함"
- Imperative mood: what changed, not how

**Verbatim examples**:

Bare commit (no args):
```
<command-message>commit</command-message>
<command-name>/commit</command-name>
```

With issue reference:
```
<command-message>commit</command-message>
<command-name>/commit</command-name>
<command-args>#19 issue number</command-args>
```

With amend request:
```
<command-message>commit</command-message>
<command-name>/commit</command-name>
<command-args>6684d99 body 메시지를 수정해줘</command-args>
```

**Reset behavior**: If the commit message is wrong or kgcrom changes their mind, they immediately reset:
```
방금 커밋도 reset해줘
```

**Takeover pattern**: After agent explains something satisfactorily, kgcrom skips acknowledgment and goes straight to commit — the commit IS the acknowledgment.
