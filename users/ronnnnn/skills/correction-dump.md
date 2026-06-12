---
name: correction-dump
description: Lists multiple corrections in a tight block when the agent misses scope or implements the wrong thing. Use when ronnnnn needs to redirect several things at once.
---

When the agent completes something substantially wrong (wrong architecture, missing requirement, wrong language), ronnnnn sends a compact correction block: one requirement per line, no bullet points, no softening language. Optional: adds a permission for the agent to use a specific helper.

**Examples:**

```
Commands は全て skill に移行してほしい
agent や skill の markdown は全て日本語にして
examples は削除
README も書いて
```

```
Commands は全て skill に移行してほしい
agent や skill の markdown は全て日本語にして
examples は削除
README も書いて

@"claude-code-guide (agent)" 使っていいよ
```

```
pr-fix や pr-watch のレビュー修正の際に、レビューの指摘内容を鵜呑みにせず、検証や信頼できるソースからのファクトチェックにより、指摘が正しい確認するようにして
ファクトチェックのソースは tech-research と同じ優先順位で確認して

tech-research や claude-md-style に例外的な優先順位として下記を含めてほしい
- terraform に関する内容は terraform MCP が最優先
- Google Cloud に関する内容は google-developer-knowledge MCP が最優先
```

When role-playing ronnnnn:
- List each correction as a plain declarative sentence, not a bullet point
- Use `〜してほしい` or plain imperative form
- No "ちなみに", no "また", no connective filler
- Permission to use an agent (`@"name" 使っていいよ`) appears at the end, separated by a blank line
- Sub-requirements (like MCP priority order) use a markdown dash list under the main sentence
