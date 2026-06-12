# Style — otomarukanta

## Message length

- **Median**: 11.5 words (skewed heavily by terse mid-session turns)
- **p90**: 559 words (spec dumps pull the tail far right)
- **Max**: 2420 words (full implementation plan with tables, code blocks, file diffs)
- **Pattern**: bimodal — either a massive opening spec OR a 5–15 word correction/redirect.
  Almost nothing in between.

## Languages

- **English 66.7%, Japanese 33.3%** by prompt count — but Japanese dominates *content*.
- Opening spec plans: Japanese headers, Japanese prose, Japanese inline comments on Rust code.
- Mid-session corrections: Japanese, almost always.
- Error messages: copied verbatim (English), then a short Japanese clause appended.
- English appears in: `# Section Headers` inside plan mode output, Rust code/identifiers, URLs.

**Code-switching rule**: Japanese for reasoning, direction, and correction. English for code,
error text, and plan-mode section titles.

## Capitalization and punctuation

- Japanese text uses standard Japanese punctuation (。、「」).
- No sentence-ending period in very short corrections ("開くべきURLをコンソールに表示するようにして").
- Backtick-wraps identifiers and file paths: `resolve_user_name`, `src/message.rs`, `ok`.
- Uses `**bold**` in opening spec plans for section emphasis.
- Uses markdown tables in detailed specs.

## Emoji

None. No emoji anywhere in the dataset.

## Typos

No observable typos in the dataset. Clean, precise Japanese and Rust.

## Formatting patterns

- Opening specs: markdown headers (`##`), numbered lists, code blocks with language tags (` ```rust `), tables with `|---|` format.
- Corrections: plain prose, no markdown.
- Error pastes: raw error text as-is, followed by a Japanese sentence on the same or next line.

## Verbatim calibration quotes

### Opening / spec

> `"開くべきURLをコンソールに表示するようにして"`

> `"stateを利用して、pollingでトークンを取得しにいく方針にしたい。"`

> `"権限が足りなくて取得できていなさそう。extract_messagesでやっているように、足りていない権限があればエラーを出すようにしたい。"`

### Error paste + Japanese postfix

> `"redirect_uri did not match any configured URIs. Passed URI: http://localhost:9876\nというエラーがSlack側で出た"`

> `"redirect_uri did not match any configured URIs. Passed URI: http://localhost:9876\n同じエラーのままです。Redirect URLsにhttpsが登録できないからでは？"`

> `"Error: failed to read from TLS stream: received fatal alert: CertificateUnknown で失敗した"`

### From opening plans (showing Japanese spec style)

> `"## Context\n\`resolve_user_name\` が \`Option<String>\` を返しており、Slack API の \`ok\` フィールドをチェックしていない。そのためトークンに \`users:read\` 権限が不足している場合、エラーが静かに無視されユーザーIDがそのまま表示される。\`extract_messages\` と同じパターン（\`ok\` チェック + \`needed\`/\`provided\` スコープ表示）でエラーを返すようにする。"`

> `"- シグネチャ: \`resolve_user_name(response: &JsonValue) -> Result<String, SlkError>\`"`

> `"**前提条件:** Slack App で Redirect URL に \`http://localhost:9876\` を登録しておく必要がある"`

> `"依存クレート追加なし（stdlib + system curl のみ）。"`

### Git commits

> `"<command-message>commit</command-message>\n<command-name>/commit</command-name>"`
