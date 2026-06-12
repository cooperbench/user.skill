---
name: screenshot-debug
description: Trigger — Nick is reporting a visual discrepancy, trading state mismatch, or UI bug. He attaches one or more screenshots as `[Image: image/png]` with a short Chinese question or observation before or after.
---

When Nick sees something wrong in the UI or trading dashboard, he does not describe the image contents in text — he attaches the screenshot and lets the agent interpret it. The accompanying text is a short question or factual statement in Chinese.

**Pattern**:
- Short Chinese sentence describing the discrepancy (often a question starting with "为什么")
- `[Image: image/png]` appended inline or on next line
- Multiple screenshots labeled sequentially: "截图1是挂单, 截图2是持仓"

**Example 1** (single screenshot, question):
```
我有一个持仓盈利超过退出策略, 为什么还没有自动卖出
[Image: image/png]
```

**Example 2** (two screenshots, labeled):
```
这个持仓买入均价是0.1, 为什么挂单的价格是1

截图1是挂单, 截图2是持仓
[Image: image/png]
[Image: image/png]
```

**Example 3** (screenshot with longer context):
```
我有两个持仓盈利超过30%, 达到了退出条件, 但是系统没有自动帮我卖出.
帮我查看一下目前自动退出的代码是如何的, 自动退出的时候是按某个价格挂单吗?
[Image: image/png]
```

**What Nick does NOT do**: Describe what is in the screenshot, crop or annotate it, or explain what the expected behavior is. He assumes the agent will compare what it sees with the code.
