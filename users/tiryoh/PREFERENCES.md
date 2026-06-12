# Preferences

## What triggers correction (23.5% of prompts)

- **Wrong metadata in generated files**: Incorrect year in LICENSE → corrected with bare fact: `"2026です"`
- **Role/speaker confusion in display**: Agent and User messages mixed up → `"transcriptの表示でAgentとUserが混同されています。確認して"`
- **Wrong output language**: Agent generates Japanese README when English was wanted → `"READMEを英語にして。日本語版についてはREADME.jp.mdにしてREADMEからリンクするようにして"`
- Does not negotiate; correction is a directive, not a discussion

## What triggers failure reports (11.8% of prompts)

- **Visual glitches**: Describes a transient display anomaly casually: `"claudeの表示が一瞬おかしくなったのだけど、理由はわかりますか？表示は消えてしまいました"`
- **Stale or partial data shown**: Cites a specific commit hash, describes the discrepancy between preview and detail view, asks why
- Reports symptoms only; does not paste logs, stack traces, or error output

## What satisfies

- Autonomous execution without needing follow-up questions
- Agent correctly stages and commits exactly the specified files/directories
- Concise summaries when explicitly requested (`"概要をまとめてもらえますか"`)
- Agent recognizes when something is an upstream issue and explains clearly

## Workflow habits

- **Not test-driven**: No test-related prompts observed across all sessions
- **Commit-driven**: Explicit commit requests after each meaningful unit of work
- **No planning phase**: Jumps straight from spec dump to implementation; no "let's outline first"
- **Delegates entirely**: Once direction is given, expects autonomous end-to-end execution
- **Asks for summary after debugging**: After a difficult or winding session, requests a recap
- **Incremental additions**: After committing, tacks on small follow-up tasks one at a time (`"@docs/screen1.png これも埋め込んで"`, `"MIT LicenseのLICENSEファイルも置いて"`)

## Tool and stack preferences

- Uses Claude Code (50%), OpenCode (33%), claude-code (17%) — tool-agnostic
- Go for backend viewer code (inferred from package paths `viewer/internal/...` in session context)
- Git-centric workflow: branches, commit hooks, and commit hashes are first-class references
- English README as primary with Japanese translation linked (not the reverse)
- MIT License preferred for open source (evidenced by explicit request)
