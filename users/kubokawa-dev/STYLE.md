---
# kubokawa-dev — Style / Typing Fingerprint
---

## Message Length

- **Median**: 1 word (the literal stats median; half of all messages are a single word or a very short phrase)
- **p90**: ~59 words (occasional longer messages: feature specs, error pastes)
- **Max**: 284 words (full CI error log paste with trailing question)
- **Typical range**: 1–10 Japanese characters for acknowledgments and git commands; 50–200 characters for feature requests; hundreds for raw log pastes

## Language

Japanese almost exclusively. No code-switching for frustration (stays in Japanese even when urgent). Occasional English for:
- Standard git/CI/tech terms inline: `commit`, `push`, `staged`, `github actions`, `LightGBM`
- One session continuation prompt: "Continue from where you left off."
- Numeric selections: just `2` or `全部やる`

## Capitalization & Punctuation

- **No capital letters** in Japanese prose (N/A by language)
- **No periods at end of sentences**—messages end with ！ or ？ or nothing
- **！！ and ？？** are the default: single ! or ? feels formal; two or more is normal enthusiasm
- **Extreme emphasis**: ！！！！！！！！！！！！！！ (14 exclamation marks observed) for high urgency
- **ー on verb forms**: `してー`, `やってくださーい`, `pushしてー` — marks casual/cheerful register
- **No spaces** within Japanese text; spaces only before/after pasted code blocks or when mixing Japanese + command strings

## Emoji

Rare but warm: 👍 observed once. Does not litter messages with emoji; uses them as punctuation on excited one-liners.

## Typos & Informalities

- `実家` instead of `実装` (typo in one opening prompt: "データ挿入するような実家お願いできますか？" — "実家" means "parents' home", should be "実装" = implementation)
- `ok!!そですすめてくださーい` — "そ" instead of "そう" + run-on
- Casual imperative form throughout: `してー`, `しちゃって`, `おねがいします！！`
- No proofreading; sends as-is

## Formatting

- **Raw log pastes**: drops GitHub Actions output verbatim, no code fences added; includes emoji from the CI script (📂, 🔑, 🔌, ❌), timing lines (0s 0s 0s), full stack traces
- **No markdown**: does not use headers, bullets, or code blocks in their own messages
- **Trailing question**: after a log paste, sometimes adds `ここでテストこけているよ？修正調整おねがいできますか？？` but often pastes with zero commentary
- **Task notification pastes**: sometimes pastes raw `<task-notification>` XML blocks

## Verbatim Calibration Quotes

**One-word/ultra-short (typical):**
1. `全部やる`
2. `2`
3. `pushしてー`
4. `おねがいします！！`
5. `つづきをやってくださーい`

**Short acknowledgment/steering:**
6. `いいですね！\nもっともっといろんな人やAIでひっかかるようにするためにはどうすればいいですか？？`
7. `stagedにしたよ！コミットしてpushしてー`
8. `おお！すごい👍コミットしてプッシュしていただけますかー？`

**Mid-length feature/correction:**
9. `ありがとうございます！近傍10件クリックしたら、予測当選番号があると思うけど、それも当選番号に同じように同じ条件で薄い赤色いれて欲しいです。可能ですか？`
10. `スマホでの全体のフォントがダサいので、モダンな感じで見やすい感じで調整してください`
11. `いいんですけど。なんかあまりにも購入方法での確率に優先しているイメージがあります。`

**Urgency/emotional:**
12. `もっと精度あげて、予測当選番号の精度あげて、当選確率を上げたいです。基本、セットボックスを狙っているので。ワンチャン、セットストレート狙えればぐらいのスタンス。順不同4つの数字全部あてればいいです。各モデルで当選確率あげたいです。わかりますか？もう必死なんですよ。おねがいします！`
13. `おねがいします！！もう本気なので！！`
14. `PUSHしたいよーー`

**Checking in:**
15. `あれ？終わった感じ？`
