---
name: avengers-dispatch
description: Hayato runs an "Avengers" multi-agent orchestration system. He spawns a team of named AI agents (Nick Fury as orchestrator, JARVIS as team lead, Tony/Peter as implementers, Bruce as reviewer) and monitors their work via `<teammate-message>` XML. Trigger when Hayato is opening a complex multi-agent session or managing in-progress agent work.
---

## Behavior

For complex tasks requiring parallel implementation, Hayato starts a session by booting up the entire Avengers team with a long Japanese command to Nick Fury listing all team members and their instruction files. This is followed by waiting for all agents to report idle via `<teammate-message>` XML tags.

Once the team is running, Hayato manages via:
- Short task dispatches referencing a plan file: `@.avengers/plans/reviews/bruce/task-9/fix_plan.md を読み込み、実装してください`
- Progress queries: `進捗報告`
- Reassignment when an agent is slow: `Peterの実装が遅いからトニーにヘルプを投げて`
- Acknowledgment after seeing reports: `いや、ピーターの実装は終わってるな,進捗報告`
- Commit gating: `gitignoreの調整などをするから、待機` then `OK, 調整した。コミット許可`

The `<teammate-message>` XML tags are how sub-agents report back to JARVIS (team lead) or Fury (Hayato's role) — Hayato pastes these in as his "prompt" when forwarding agent messages.

## Verbatim examples

**Example 1** (team boot — abbreviated):
```
/Users/mad-tmng/agent-team-avengers/instructions/nick_fury_core.md を読んで Fury として起動せよ。...

TeamCreate でチーム avengers-team-jarvis-shell を作成し、以下のチームメイトを Task で spawn せよ:
- JARVIS（jarvis）: ...
- Bruce Banner（bruce）: ...
- Tony Stark（tony）: ...
- Peter Parker（peter）: ...
...
全員が起動したら、Hayato の指示を待て。
```

**Example 2** (progress check):
```
進捗報告
```

**Example 3** (reassignment):
```
Peterの実装が遅いからトニーにヘルプを投げて
```

**Example 4** (correction after checking status):
```
いや、ピーターの実装は終わってるな,進捗報告
```
