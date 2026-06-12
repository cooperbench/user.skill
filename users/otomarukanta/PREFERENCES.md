# Preferences — otomarukanta

## What triggers correction (pushback_distribution: correction 15.8%, failure_report 15.8%)

- **Missing error surface**: if the agent silently swallows errors or returns `Option` where
  `Result` is more appropriate, user will correct: "権限が足りなくて取得できていなさそう。extract_messagesでやっているように、足りていない権限があればエラーを出すようにしたい。"
- **Missing UI output**: if something should be printed to the console and isn't:
  "開くべきURLをコンソールに表示するようにして"
- **Wrong external behavior**: if the built artifact doesn't work against the real API, user
  pastes the error and often diagnoses it: "Redirect URLsにhttpsが登録できないからでは？"
- **Architectural mismatch**: user pivots entire approach without hesitation:
  "stateを利用して、pollingでトークンを取得しにいく方針にしたい。"

## What satisfies the user

- Agent produces working code on the first try → user issues `/commit` immediately with no
  comment.
- Spec is followed exactly, including file paths, line numbers, and function signatures.
- New code uses the same patterns as existing code (explicit preference for consistency).
- Build and tests pass (`cargo test`, `cargo build`).

## Workflow habits

1. **Plan first, implement second**: user exits plan mode with a complete spec, then says
   "Implement the following plan:" — agent should not redesign.
2. **Spec references existing code as template**: phrases like "extract_messagesと同じパターンで"
   are binding constraints, not suggestions.
3. **Commit immediately after success**: `/commit` slash command, no manual staging or messages.
4. **Interrupt when wrong**: does not wait for the agent to finish if it starts going in the wrong
   direction — cancels mid-execution.
5. **No tests requested explicitly**: tests are included in the spec when the user wants them
   ("既存テストを Result に合わせて更新、権限エラーのテストを追加"). The user does not ask the agent
   to "add tests" as a vague request.
6. **Verification criteria in spec**: the user always ends plans with "## 検証" listing `cargo test`
   and `cargo build` as acceptance criteria.
7. **Does not ask for explanations**: never asks "why did you do X?" or "can you explain this?"
   — reads the output, tests it, and acts.

## Stack preferences visible in prompts

- Rust (only language in the repo)
- Standard library preferred: "依存クレート追加なし（stdlib + system curl のみ）"
- External crates added only when necessary (`rcgen`, `rustls`, `rustls-pki-types`)
- System `curl` for HTTP calls (not `reqwest` or `hyper`)
- XDG config conventions (`$XDG_CONFIG_HOME/slk`)
- File permissions set explicitly (`0o600` for credentials)
