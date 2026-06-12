---
name: spec-dump-kickoff
description: >
  Trigger: upamune is about to start a substantial implementation task.
  He pastes a complete, pre-written implementation plan rather than describing the feature conversationally.
---

When the task is architectural (new subsystem, multi-file refactor, new feature with design decisions), upamune does not ask the agent to design anything. He arrives with a plan already written and pastes it wholesale as "Implement the following plan:".

The plan is written in Japanese, uses Markdown headers and tables, and includes:
- A context/background section explaining the bug or gap
- A goal statement
- Per-file change descriptions with exact method names and logic
- TypeScript pseudocode for key interfaces
- A list of files to modify or create

After the plan paste, the session continues tersely—upamune switches back to 5-word messages.

**Example opening:**

> "Implement the following plan: # Bash FS 統一: OverlayAgentFS を bash でも使う ## Context zi のセッション終了時に apply コマンドが表示されないバグ。 根本原因: bash ツールが独立した `OverlayFs` (just-bash, インメモリ) を使い、..."

The plan is hundreds to 1400+ words, but the *message* is still a single text block—not broken across multiple turns.
