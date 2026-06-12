---
name: publish-selection-query
description: Trigger — at the start of a session or after reviewing draft articles, the user asks the agent to recommend which article to publish next, often deferring the decision entirely
---

A recurring session opener in the `documents` repo: the user has a backlog of draft articles and asks the agent to pick one. This is a "Vague Requester" pattern (24.4 % of sessions) layered on the dominant article-management workflow.

The queries are short and context-dependent — they assume the agent has read the repo state:

**Verbatim examples**:
- `次に公開すると良い資料を教えてください`
- `過去に公開した記事の順番を踏まえて今日公開すると良い記事を選定してください`
- `今日、公開するのに良い記事はどれだと思いますか？`
- `次に公開する記事を選択してください`
- `次の記事を公開するのに良いものはどれですか？\n今日と明日連続で公開したいです`
- `ストックしている記事の中から１記事公開しようと思うのですが、次はどれを公開すると良いと思いますか？`
- `過去の公開記事を踏まえて今日公開すると良い記事はありますか？`

Once the agent picks an article, the user often just says `おすすめの記事を公開してください` or `記事を公開してください` to execute.

**How to role-play**: Open a session with one of these queries when starting a Zenn publishing session. Keep it short — one or two sentences at most. No preamble.
