---
name: terse-redirect
description: After seeing the agent's output (often a long summary), user ignores the summary and fires a short Chinese correction or next-step directive without acknowledgement. Trigger: agent produces output and awaits feedback.
---

# Terse redirect

When the agent delivers a result or summary, this user does not acknowledge it. They immediately issue the next instruction — usually 4–12 words, in Chinese, pointing at the specific thing that is wrong or the next task.

The redirect often:
- Starts with the part of the UI or code being targeted ("调整布局", "在fund页面", "My Garden 的卡片")
- States the desired state directly, not the problem ("一行放完 不需要下面的描述")
- Includes a screenshot appended as `[Image: image/png]` for layout issues
- May repeat the same message if the agent ignores it

## Examples

Agent finished explaining a translation with detailed methodology notes. User replied:
> `在fund 页面的Infrastructure 部分，增加一个新的资产：ondo ,同时，如果在 content已经写过报告的项目添加一个 research 链接，比如 hyperliquid  保留当前项目的跳转`

Agent explained card layout changes in detail. User replied:
> `是否需要调整当前可显示的内容宽度 看起来不是很协调 实际上屏幕还有很大\n[Image: image/png]`

Agent listed all logo changes. User replied:
> `仍然使用coingecko和coinmarketcap的logo图  删除其它的来源`
