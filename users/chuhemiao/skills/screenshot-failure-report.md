---
name: screenshot-failure-report
description: When a visual or rendering bug occurs, user attaches a screenshot with minimal or zero written description. Trigger: something doesn't render correctly in the browser or CI.
---

# Screenshot failure report

This user never describes rendering bugs in prose. They attach a screenshot and write 0–8 words. For CLI/build errors they paste the raw terminal output verbatim, also with minimal framing.

For visual issues:
- Message ends with `[Image: image/png]`
- Written context is optional and brief: "在fund的页面中，ai筛选出现了问题，当前分类下只有一个资产"
- Sometimes the screenshot is the entire message

For build/runtime errors:
- Pastes the full stack trace or error output without paraphrasing
- May add a very short Chinese note before: "有个waring\n[Image: image/png]"
- Sometimes the error IS the message (no leading text)

## Examples

Visual bug, with brief note:
> `在fund的页面中，ai筛选出现了问题，当前分类下只有一个资产\n[Image: image/png]`

Screenshot only (no words):
> `[Image: source: /Users/kk/.claude/image-cache/1a7149b7-7ef7-48d0-ad8a-d37add1826b2/2.png]`

Duplicate rendering bug with two images:
> `每个部分切换都出现了两次 Hyperliquid Quality\n\nCrypto\n\nHYPE\n[Image: image/png]\n[Image: image/png]`

Raw error paste (no framing):
> `✓ Ready in 399ms\n⨯ ./src/components/mermaid.tsx:13:5\nModule not found: Can't resolve 'mermaid'\n  11 |...`

Minimal text with error:
> `无法渲染`
