---
session_id: "lyston11/Codex_Bundles|019e4db9-5c1b-79c3-9b89-baa090b93375"
developer: "gh:lyston11"
split: train
source: crawl
repo: lyston11/Codex_Bundles
start_time: "2026-05-22T03:27:34.297Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

{"人设":"变种人妈妈二代","任务":"a2产品","字数":"评论-短","业务规则":"a2产品","扰动规则":"a2产品","评论切角":"产品切角-儿童奶粉-带引流","生文输出格式":"生文输出格式-评论"}

这是飞书表格的B2的内容
我怎么在另一个表格中 使用函数取出 "评论切角":"产品切角-儿童奶粉-带引流" 中的 产品切角-儿童奶粉-带引流
参考：=REGEXEXTRACT(B2,""评论切角":\s*([^;]+)")

> AGENT

用这个就行：

```excel
=REGEXEXTRACT(B2,"""评论切角""\s*:\s*""([^""]+)""")
```

会提取出：

```text
产品切角-儿童奶粉-带引流
```

如果是在另一个工作表里取，比如原数据在 `Sheet1` 的 `B2`：

```excel
=REGEXEXTRACT(Sheet1!B2,"""评论切角""\s*:\s*""([^""]+)""")
```

你原来的 `([^;]+)` 是按分号 `;` 截取，但这段内容是 JSON 风格，值被双引号包住，所以更适合用 `([^""]+)`，意思是一直取到下一个双引号之前。
