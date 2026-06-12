---
name: page-feedback-redirect
description: >
  Trigger: user sends a structured `## Page Feedback: /path` block with numbered items, React
  component tree, and Chinese-language feedback. This is the dominant message format — use it
  for almost all design change requests.
---

# Page Feedback Redirect

The user has a visual feedback MCP tool that captures live browser state and formats it as a
structured block. They send this instead of typing a description. The message looks like:

```
## Page Feedback: /posts/some-slug
**Viewport:** 1512×861

### 1. <ComponentTree> element description
**Location:** .css > .selector > .path
**React:** <ComponentA> <ComponentB> <TargetComponent>
**Feedback:** 中文的反馈内容，可能是很具体的 CSS 改动
```

**Behavior:**
- The feedback content is in Chinese (usually) and is always specific: exact font name, exact px value, exact color hex, exact behavior description.
- Multiple items are numbered (### 1, ### 2, ...).
- Images may be attached (`[Image: image/png]`) as reference — no description given.
- The user does NOT explain why. They state what to change.

**How to produce this as maoxiaoke:**

Select a relevant page path and construct the block exactly. Write feedback in Chinese. Reference the React component tree path and CSS selector path. Be surgical — one to four specific items max.

**Example 1 — typography tweak:**
> "## Page Feedback: /posts/advanced-guide-to-ai-programming\n\n1. **<Container> ... time**: 这个 letter-space 改成 1px"

**Example 2 — multi-item:**
> "## Page Feedback: /\n\n1. **paragraph: \"nazha\"**: 在 nazha 的前面和 update 的前面加一个 avatar\n2. **paragraph: \"nazha\"**: 字体换成 https://fonts.google.com/specimen/Gaegu\n3. **paragraph: \"nazha\"**: 暗黑按钮，rss 订阅 和 X 不要移除"
