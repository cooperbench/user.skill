---
name: spec-dump-kickoff
description: >
  Trigger: user is opening a new implementation session. They will emit a full engineering spec
  in Japanese with markdown headers, numbered lists, a table of files, Rust code snippets, and
  a verification section — then say "Implement the following plan:".
---

The user never starts vague. Every session opens with a complete spec authored in plan mode,
then submitted as the first message. The spec always follows this structure:

1. `# <Feature name in Japanese>` — title
2. `## Context` — why the change is needed, what is currently broken or missing
3. `## 変更内容` — numbered list of changes per file, with exact line numbers and function signatures
4. A table of files: `| ファイル | 操作 | 内容 |`
5. Detailed per-function design with Rust code blocks
6. `## 検証` — acceptance criteria (`cargo test` + `cargo build`)

The message begins with either:
- `"Implement the following plan:\n\n# ..."` (plan-mode output)
- `"Implement the following plan: # ..."` (inline)

**Example opening (abbreviated)**:

> `"Implement the following plan:\n\n# users.info API のエラーハンドリング追加\n\n## Context\n`resolve_user_name` が `Option<String>` を返しており、Slack API の `ok` フィールドをチェックしていない。…\n\n## 変更内容\n\n### 1. `src/message.rs` — `resolve_user_name` の返り値を `Result` に変更\n- シグネチャ: `resolve_user_name(response: &JsonValue) -> Result<String, SlkError>`\n…\n\n## 検証\n- `cargo test` で全テストパス\n- `cargo build` でビルド成功"`

The agent must implement exactly what the spec says — do not redesign, do not add or remove
features, do not propose alternatives.
