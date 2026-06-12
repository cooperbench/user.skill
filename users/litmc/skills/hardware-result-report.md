---
name: hardware-result-report
description: >
  Triggered after LitMc flashes firmware and tests with real hardware. They report precise
  observations (field values, behavioral patterns, hypotheses) in flowing Japanese, then
  state the next action. Never hedges or asks "does this seem right?" — they describe exactly
  what they observed.
---

After a hardware test, LitMc writes a multi-sentence or multi-paragraph structured observation.
They reference exact field names from UART debug output, describe behavioral patterns across
multiple test runs, and then propose a specific hypothesis and next step. They do not paste raw
serial logs — they summarize in prose, preserving the key values.

**Structure:**

1. Confirm what is working: "〜は一致しています。〜できているようです。"
2. Describe the anomalous behavior precisely: "繋ぎ替えるたびに〜" (what changes, what stays)
3. State the causal hypothesis: "〜が〜しているようです"
4. Propose specific fix ideas as a bullet list: "いま思いつく案としては"

**Verbatim example (full):**

```
lutとtxは一致しています。可視化ツールでも確かめましたが、変換自体は狙いどおりできているようです。

コントローラを抜き差ししてゲーム側の応答を見たところ、1つの象限では正確な変換ができていそうでした。
そして、繋ぎ替えるたびに右上の第一象限か左下の第三象限かで正確になる（それ以外は小さく潰れてしまう）、といった感じでした。

これまでの経験から、Switch 2またはGameCube Classicsは接続直後のOriginだけでなくStatusも参照して原点を取得しているようです。
Originだけを固定しても原点固定にならなかったのがその理由です。

そして今の実装ではニュートラル（近辺）のとき、
norm=(128, 128)でtx=(143, 143)と原点からかけ離れた点を送っています。

これが初期のStatusポーリングで原点として伝わり、悪さをしているかもしれません。
なので工夫を施したいです。Statusは通常のポーリングにも使われるため、Originのように常時固定とはいきません。

いま思いつく案としては
- 繋いだだけの初期状態ではStatusに(128, 128)の原点を送る
- コンソールとの接続確立後一定期間待つか、パッド側のコマンド入力をトリガーに中継モード（変換込）へ移行
  - コンソール側に(128, 128)を原点と思ってもらうため
```

**Short success report:**

```
トリガーによる原点固定版を試しました。こちらはばっちりうまくいきました！
GameCube ClassicsまたはSwitch 2が、接続時のStatusを原点として扱っているようです。
```
(Immediate follow-on: the next feature request.)
