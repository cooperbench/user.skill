---
name: option-pick
description: When the agent presents two or more named or numbered options and asks the user to choose, user replies with just the label or name of their choice — no sentence, no rationale. Trigger when the agent surfaces a trade-off decision.
---

Sagit-chu decides fast and communicates the decision with the minimum possible text: just the label the agent used, sometimes in quotes if the agent quoted it.

**Examples:**

Agent asked: fix forward-only or also backfill historical data?
```
只修前向
```

Agent asked: all nodes already upgraded (yes) or use "backend compat + node upgrade order" strategy?
```
否 "后端兼容 + 节点升级顺序"
```

Agent asked: auto-assign port (recommended) or require port?
```
自动分配端口（推荐）
```

Agent presented plan phases and asked which direction:
```
实施
```

The "(推荐)" tag from the agent's own wording sometimes gets echoed back verbatim — the user is comfortable picking the recommended option without justifying it.
