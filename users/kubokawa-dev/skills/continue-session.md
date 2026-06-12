---
name: continue-session
description: "Trigger: returning to a paused session, or agent appears to have stopped mid-task. User asks to continue with minimal words, sometimes switches to English."
---

kubokawa-dev often resumes sessions in progress or checks if the agent is done with a brief, casual prompt. The language for continuation can switch to English ("Continue from where you left off.") or stay in Japanese.

**Pattern**:
- Resume politely: `つづきをやってくださーい`, `このつづきをおねがいできますか？？`
- Check if done: `あれ？終わった感じ？`
- English switch (rare): `Continue from where you left off.`

**Example 1** (Japanese, cheerful):
```
つづきをやってくださーい
```

**Example 2** (English, matter-of-fact):
```
Continue from where you left off.
```

**Example 3** (checking in after silence):
```
あれ？終わった感じ？
```
