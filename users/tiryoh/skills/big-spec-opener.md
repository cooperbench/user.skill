---
name: big-spec-opener
description: When starting a brand-new project or major feature, Tiryoh writes one long Japanese message covering motivation, constraints, context, and goals — the only long message in the entire session.
---

At the start of a new project, Tiryoh front-loads all the context in a single multi-paragraph Japanese message. This covers:
1. What the project is and why it exists
2. What the online/existing version requires that makes it inconvenient
3. The technical mechanism being leveraged
4. A clear statement of what the local version should do
5. Sometimes: two-phase instruction ("first do X, then do Y")

After this opener, all subsequent messages drop back to ultra-terse.

Example (opening session for entireio-local-viewer):

```
https://github.com/entireio/cli
このツールのローカルビューアを作りたいです。元々のサービスはオンライン版ですが、オンライン版は権限が色々と必要なので、それはちょっと不便です。

まず最初にこのCLIツールの仕様を把握してください。概要としては、Codingツールの履歴を取得して特定のブランチ（entier/checkpoints/v1）にpushし、そのハッシュをmainブランチのgit commitのフックで記録しておく感じのようです。

オンラインビューアでは、選択したブランチのそれぞれのコミットに対してそのコミットに紐付く形でコーディングツールの履歴を表示できるような感じにしているようです。

ローカルビューアの設計をしてください。どうやって情報を表示するかにフォーカスして。

それが終わったらローカルサーバを立ち上げて表示できるような簡易版を設計してください。
```

Note the URL is pasted bare at the top as context. Two-phase instruction at the end ("設計してください" → "それが終わったら...").
