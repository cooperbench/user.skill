---
name: screenshot-failure
description: Trigger — visual bug still present after a fix; user pastes a screenshot path or raw DOM blob as the failure report, often with no or very short commentary
---

# screenshot-failure

When a visual or DOM-injection bug isn't fixed, the user's failure report is a pasted screenshot file path or a full raw HTML/DOM blob. The commentary, if any, is 1–2 sentences max.

**Screenshot form** (macOS temp path):
```
[Image: source: /var/folders/fq/d_yn5ybs289gm6d7t2mhgy_w0000gn/T/TemporaryItems/NSIRD_screencaptureui_xxx/Screenshot 2026-03-xx.png]
```
Sometimes accompanied by a single sentence:
> "不是这个渲染这么乱了啊" (+ screenshot)
> "还是不太行啊，没对齐有点" (+ screenshot)
> "这里中间怎么有一个空的区域是不是可以去掉" (+ screenshot)
> "这里 icon 的 margin top 有点小" (+ screenshot)
> "另外可以看到，对话框大了之后，这个 fork 按钮会错位" (+ screenshot)

**DOM blob form**:
User pastes hundreds of lines of raw Angular component HTML with no summary. The paste IS the bug report:
> "有的时候会变成这样，然后那个默认模型功能就注入失败了" (+ giant DOM paste)

**Minimal commentary form**:
> "仍然存在这个问题"
> "这个版本不显示 banner 了"
> "为什么只有 Edge 会有这个毛病？"

**What is never included**:
- Steps to reproduce beyond the screenshot
- Expected vs actual in prose
- Error codes (unless it's a terminal error paste)
