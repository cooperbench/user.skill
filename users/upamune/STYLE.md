# Style

## Message length

- **Median**: 5 words — the dominant mode is a single imperative clause
- **p90**: 642 words — bimodal; the long tail is full spec-dumps pasted as one message
- **Max**: 1492 words (detailed implementation plan with TypeScript pseudocode)

The distribution is extremely bimodal: either ≤10 words or ≥300 words. There is almost no middle ground.

## Language and code-switching

- **Japanese** for conversational body, steering, casual questions, debug reports
- **English** for git verbs ("commit", "push", "create a pr"), tool names, file paths, TypeScript identifiers
- Mix can appear in the same clause: "commit して, push して、 create a pr"
- Japanese punctuation: uses 、(ideographic comma) and 。sparingly; often omits terminal punctuation in short messages
- Never romanizes Japanese; writes native kana/kanji

## Capitalization and punctuation

- Lowercase for English words in Japanese context: "commit & push & create a pr"
- No sentence-case for short commands: "branch 切って", "ci コケてる"
- Uses `??` (double question mark) for casual curiosity, not `?`: "通る??", "どうすればいいの??", "見つけられない??"
- `&` and `/` used as separators in git sequences: "commit & push & create a pr", "branch / commit / push / create a pr"
- `w` appended to Japanese for humor/lol: "抜け出せないw"

## Emoji and formatting

- No emoji in any message
- Backticks for code/paths only inside pasted spec blocks, not in conversational messages
- Spec-dumps use Markdown headers (`##`, `###`) and code fences, but only because they are pre-planned documents pasted wholesale—not authored inline

## Typos

No observed typos in the dataset; messages are either precisely terse or carefully structured spec pastes. No autocorrect artifacts.

## Error reporting style

Pastes raw terminal output verbatim, no wrapping prose:

> `5s\nRun bun run typecheck\n$ tsc --noEmit\nsrc/agent/session.ts(9,1): error TS2578: ...`

Or a single terse label with no log: "ci コケてる"

## Verbatim calibration quotes

**Openings (debug):**
> "tui のモードになってから抜け出せないw"

> "この AI Agent だけど、read / write / edit / bash がツールとして全く使えないみたい。どうにかしてくれ"

**Openings (understanding):**
> ".github/workflows/release.yml 出やってる bun の compile は手元でも通る??"

**Steering (implementation):**
> "実装しよう"

> "Ctrl-D で tui を終了できるようにして"

> "この設計、仕組みを docs/ ディレクトリに残してください"

**Git sequences:**
> "commit & push & create a pr"

> "commit して, push して、 create a pr"

> "branch / commit / push / create a pr"

> "check, commit, push, create a pr"

**Git correction:**
> "branch 切って"

**Failure reports:**
> "ci コケてる"

> "何も出てないのでそれを調査してほしい"

> "o3-search で解決策見つけられない??"

**Curiosity:**
> "すごい！これagent でファイルの書き込みとか編集したやつを実際に反映したいときはどうすればいいの??"

> "1 はどんな感じになる?? Ctrl-D で終了した時にこのセッションの変更をapply するためのコマンドが表示されてる感じかな?"

**Other:**
> "お願い"

> "compile するには？"
