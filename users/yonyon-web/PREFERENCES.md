# Preferences — yonyon-web

## Pushback distribution

| type | rate |
|---|---|
| correction | 73.3% |
| non-pushback | 26.7% |

The user corrects the agent in nearly 3 out of 4 turns. This is structural to their workflow: they specify loosely, see the result, then steer by correction rather than spec upfront.

## What triggers correction

- **Saved too eagerly**: agent saves rows on click → user corrects to save only when a value is entered.
- **Wrong trigger semantics**: agent uses one interaction model, user wants a finer-grained one.
- **Layout shift**: noticeably bad visual behavior (`まだレイアウトシフトが発生してしまいます`).
- **Spurious defaults**: `number` input auto-fills `0` on focus → user redirects to `input type text`.
- **Incomplete scope**: agent finishes a task but an adjacent file/script needed updating → `reset.jsの内容も更新しておいて`.
- **Missing features after a partial delivery**: agent implements part of a form → user adds description field, example field, edit capability, and sort capability in one follow-up.
- **Hardcoded field they didn't ask for**: questions why `名前` column is mandatory, then steers to UUID-only identity.

## What satisfies

- Simple confirmations or status updates get no reply (non-pushback). When the user says `インストールできました` they expect the agent to continue, not summarize.
- Clean UX changes that don't shift layout or change input behavior unexpectedly.
- Features that hide engineering concepts from end users.

## Workflow habits

- **Spec-by-reaction**: opens with a vague feature intent, sees the implementation, then adds refinements. Does NOT write detailed upfront specs.
- **No planning phase**: goes straight to implementation requests; no "let's design this first".
- **Delegates all code**: never suggests a specific approach in code; trusts the agent to choose implementation details.
- **Manual confirmation loop**: when a dependency install or manual step is needed, they offer (`こちらでインストールしましょうか？`) and report back (`インストールできました`).
- **Git at end**: `コミットして` — issues a commit command without specifying a message; expects the agent to compose one.
- **No explanation requests**: does not ask "how does this work?"; asks "why is this designed this way?" (`名前列が必ずあるのはなぜ？`) only when a design choice seems wrong to them.
- **Persistent on unfixed bugs**: if a fix doesn't resolve the issue, comes back with `まだ〜` (still...).

## Stack / tool preferences visible in prompts

- **Svelte** frontend (SpreadsheetTable.svelte is the central component)
- **Node.js** scripts for data management
- **Markdown** files for wiki content storage
- Favors `input type text` over `type number` for UX reasons
- Prefers UUID-based row identity over user-visible name fields
- Wants UI labels in plain Japanese, not engineer vocabulary
