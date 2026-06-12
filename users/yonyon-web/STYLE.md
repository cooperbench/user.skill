# Style — yonyon-web

## Quantitative fingerprint

| metric | value |
|---|---|
| median prompt length | 21 words |
| p90 prompt length | 22 words |
| max prompt length | 23 words |
| session turns (median) | 2.5 |
| sessions | 8 total |

Word counts are in Japanese morphological units; in raw characters most prompts are 20–60 chars.

## Language

- **100% Japanese** — no English words, no code-switching, not even variable names quoted in English.
- Exception: technical tokens that exist natively as ASCII appear inline without quotes: `reset.js`, `input type text`, `number`, `ID`.
- Writing system mix: hiragana, katakana, kanji — standard Japanese prose, no romaji.

## Message length patterns

- **Shortest messages**: 3–6 chars for git or status (`コミットして`, `インストールできました`).
- **Typical corrections**: 1–2 sentences, 20–40 chars.
- **Long messages**: multi-item feature lists with explicit line breaks; still no longer than ~120 chars total.
- **Never bullet lists or markdown** inside their own messages.

## Casing and punctuation

- Uses `。` (Japanese full stop) to end complete thoughts; sometimes omits it in short redirects.
- Uses `。\n` or `\n\n` between items in a multi-request dump.
- No kaomoji, no emoji.
- No bold, no headers, no code fences in their own prompts.

## Typo / fragment patterns

- Cuts off mid-sentence when an idea arrives quickly: `識別子が必要ということ？であればランダムのIDde` — the trailing `de` is an unfinished `で` (particle).
- Does not go back to correct typos.
- Uses `さい` for `際` (homophone typo): `属性を追加するさい` (when adding attributes).

## Calibration quotes

**Openings — feature request:**
> `属性に画像を追加する仕組みを入れたい。画像を新規投稿もしくはすでに投稿されている画像を選ぶ形にしたい`

**Opening — terse git:**
> `コミットして`

**Opening — new script:**
> `dataやwikiを初期状態に戻すnodeスクリプトを作成して`

**Opening — UX audit:**
> `このシステムは非エンジニアが使うものなのでエンジニア用語をUI上にできるだけ出さないようにしたい。改善できるところを探して`

**Mid-session — manual step offer:**
> `こちらでインストールしましょうか？`

**Mid-session — confirmation:**
> `インストールできました`

**Mid-session — terse redirect:**
> `reset.jsの内容も更新しておいて`

**Mid-session — UX behavioral spec:**
> `クリックじゃなくて値を入れたときだけ保存にしてほしい`

**Mid-session — design challenge:**
> `名前列が必ずあるのはなぜ？`

**Mid-session — cut-off idea with typo:**
> `識別子が必要ということ？であればランダムのIDde`

**Mid-session — detailed UX correction (longest message):**
> `numberはフォーカスすると自動で0入っちゃうので数値でもinput type textにしよう。さらにフォーカスするとinput要素に切り替わり横幅が変わってしまうのが変なのでセルのサイズは変わらないようにして`

**Mid-session — persistent bug report:**
> `まだレイアウトシフトが発生してしまいます`

**Mid-session — multi-item feature dump:**
> `属性を追加するさい属性の説明も入力できる必要があると思う。`
> `また入力例とかを入れれるといいよね`
> ``
> `あと属性を修正できるようにして。`
> ``
> `さらに属性の順番を並び替えれるようにもしたい`
